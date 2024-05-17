import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url'; // Importe a função fileURLToPath
import morgan from 'morgan';
import helmet from 'helmet';
import cors from 'cors';
import dotenv from 'dotenv';
import expressStaticGzip from 'express-static-gzip';
import fs from 'fs';

// Carregar o arquivo JSON
const rawConfig = fs.readFileSync('keys.json');
const config = JSON.parse(rawConfig);

// Configurar variáveis de ambiente
dotenv.config();

// Obtendo o caminho do diretório atual
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Criar uma instância do aplicativo Express
const app = express();

// Middlewares
app.use(helmet()); // Usar Helmet para segurança básica
app.use(cors()); // Habilitar CORS para todas as rotas
app.use(morgan('dev')); // Configurar o morgan para logar requisições

// Servir arquivos estáticos com cache
app.use('/', expressStaticGzip(path.join(__dirname, 'public')));

// Rota para a página inicial
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Rota para outra página
app.get('/outra-rota', (req, res) => {
  res.send('Esta é outra rota!');
});

// Tratamento de erros
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Algo deu errado!');
});

// Rota não encontrada
app.use((req, res) => {
  res.status(404).send('Página não encontrada');
});

// Definir a porta para o servidor
const PORT = process.env.PORT || 3000;

// Iniciar o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
