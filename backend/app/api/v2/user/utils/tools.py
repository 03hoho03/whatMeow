import bcrypt
import secrets
import string
import smtplib
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jose import jwt

from app.config import settings
from ..schema import UserPayload


async def create_hashed_password(password):
    salt_value = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt_value)


async def is_password_correct(data, user):
    stat = bcrypt.checkpw(data.password.encode(), user.password.encode())
    if stat:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Information")


async def create_access_token(user):
    access_expire = datetime.now() + timedelta(days=1)
    user_access_info = UserPayload(**user.__dict__, exp=access_expire)

    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)

    return access_token


async def create_refresh_token(user):
    refresh_expire = datetime.now() + timedelta(days=14)
    user_refresh_info = UserPayload(**user.__dict__, exp=refresh_expire)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    return refresh_token


async def get_google_redirect_uri():
    return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI_V2}&response_type=code&scope=openid email profile"


async def get_kakao_redirect_url():
    return f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI_V2}&response_type=code"


async def make_return_dict(user, id, data):
    is_owner = True if user.id == id else False
    if id:
        follow = False
        for f in data["followers"]:
            if id == f.fromUserId:
                follow = True
                break
    else:
        follow = False

    _dict = {
        "userId": user.id,
        "nickname": user.nickname,
        "profileThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        "postCount": len(data["posts"]),
        "explain": user.explain if user.explain else "",
        "follow": {
            "followerCount": len(data["followers"]),
            "followingCount": len(data["followings"]),
            "isFollowing": follow,
        },
        "cats": [
            {
                "catName": cat.catName,
                "catId": cat.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{cat.image}",
            }
            for cat in data["cats"]
        ],
        "posts": [
            {
                "postId": post.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/post/{user.id}/{post.id}/0.jpg",
            }
            for post in data["posts"]
        ],
        "owner": is_owner,
    }

    return _dict


async def make_cat_ids(cats):
    return [{"catId": cat.id, "catName": cat.catName} for cat in cats]


async def make_random_code_for_register():
    digit_and_alpha = string.ascii_letters + string.digits
    return "".join(secrets.choice(digit_and_alpha) for _ in range(6))


async def template(code):
    return """
        <table cellpadding="0" cellspacing="0" border="0" style="width:500px;padding-top:60px">
            <tbody>
                <tr>
                <td><img src="https://{}.s3.ap-northeast-2.amazonaws.com/email.png" width="99" height="54" border="0" alt="WhatMeow" class="CToWUd" data-bit="iit"></a></td>
                </tr>
                <tr>
                <td
                    style="padding-top:25px;font:bold 32px 'Malgun Gothic',dotum,verdana,serif;color:#17191d;letter-spacing:-1.5px">
                    WhatMeow 회원가입 코드 안내</td>
                </tr>
                <tr>
                <td
                    style="padding:20px 0 30px;font:14px 'Malgun Gothic',dotum,verdana,serif;color:#4a4e57;letter-spacing:-0.7px;line-height:1.71">
                    안녕하세요, <strong style="color:#17191d;word-break:break-all;word-wrap:break-word">신규 회원가입</strong> 고객님<br>
                    고객님의 인증 코드는 <strong style="color:#17191d;word-break:break-all;word-wrap:break-word">{}</strong> 입니다.
                </td>
                </tr>
            </tbody>
        </table>
    """.format(
        settings.BUCKET_NAME, code
    )


async def make_email_text(receiverEmail, code):
    content = await template(code)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "%s" % "[WhatMeow] 이메일 인증 코드 안내"
    msg["From"] = "fnzksxl@gmail.com"
    msg["To"] = receiverEmail

    html = MIMEText(content, "html")
    msg.attach(html)

    return msg.as_string()


async def stmp_connect_and_send(receiverEmail, msg):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(settings.EMAIL_SENDER, settings.EMAIL_PW)

    smtp.sendmail(settings.EMAIL_SENDER, receiverEmail, msg)
    smtp.quit()
