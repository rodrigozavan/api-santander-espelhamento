module.exports = {
  apps: [
    {
      name: 'api-santander-espelhamento',
      script: 'uv',
      args: 'run uvicorn main:app --host 0.0.0.0 --port 8000',
      cwd: './',
      instances: 4,
      exec_mode: 'cluster',
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development',
        PYTHONUNBUFFERED: '1'
      },
      env_production: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      },
      error_file: './logs/pm2-error.log',
      out_file: './logs/pm2-out.log',
      log_file: './logs/pm2-combined.log',
      time: true,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      listen_timeout: 3000,
      kill_timeout: 5000
    }
  ]
};
