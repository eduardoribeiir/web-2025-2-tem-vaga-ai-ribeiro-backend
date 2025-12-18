const app = require('./app');
const { migrate } = require('./config/db');
const { port } = require('./config/env');

try {
  migrate();
  app.listen(port, () => {
    console.log(`API rodando na porta ${port}`);
  });
} catch (err) {
  console.error('Erro ao iniciar banco:', err);
  process.exit(1);
}
