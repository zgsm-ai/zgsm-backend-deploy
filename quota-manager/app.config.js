// Production environment configuration
window.APP_CONFIG = {
  // API configuration
  api: {
    baseURL: '/api',
    timeout: 30000,
    enableMock: false
  },

  // Application configuration
  app: {
    name: 'Quota Manager',
    version: '1.0.0',
    description: 'AI Quota Management System',
    author: 'ShenMA AI Team'
  },

  // Feature configuration
  features: {
    userAudit: true,
    strategyManagement: true,
    settings: true,
    realTimeMonitoring: true
  },

  // Theme configuration
  theme: {
    primaryColor: '#409EFF',
    layout: 'classic'
  }
};