module.exports = async (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    webpack: (config, { dev }) => {
      if (dev) {
        config.devServer = {
          port: 3001,
          allowedHosts: ['local.whatmeow.shop'],
        }
        config.watchOptions = {
          poll: 1000,
          aggregateTimeout: 300,
        }
      }

      return config
    },
  }
  return nextConfig
}
