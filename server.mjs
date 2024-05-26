import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url'; // Importe a função fileURLToPath
import morgan from 'morgan';
import helmet from 'helmet';
import cors from 'cors';
import dotenv from 'dotenv';
import expressStaticGzip from 'express-static-gzip';
import fs from 'fs';
import { exec } from 'child_process';

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
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "https://unpkg.com"],
        imgSrc: ["'self'", 'data:', 'https://tile.openstreetmap.org', 'https://unpkg.com']
      }
    }
  })
);

app.use(cors()); // Habilitar CORS para todas as rotas
app.use(morgan('dev')); // Configurar o morgan para logar requisições

// Servir arquivos estáticos com cache
app.use('/', expressStaticGzip(path.join(__dirname, 'public')));

// Rota para a página inicial
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Rota para a página de formulario
app.get('/forms', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'formulario.html'));
});

// Rota para outra página
app.get('/outra-rota', (req, res) => {
  res.send('Esta é outra rota!');
});

// Rota para obter os dados do JSON
app.get('/data', (req, res) => {
  fs.readFile('data.json', 'utf8', (err, data) => {
    if (err) {
      res.status(500).send('Erro ao ler o arquivo JSON');
    } else {
      res.json(JSON.parse(data));
    }
  });
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

// Função para executar o script Python e atualizar o JSON
const updateData = () => {
  exec('python Fetch.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Erro ao executar o script Python: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Erro no script Python: ${stderr}`);
      return;
    }
    console.log(`Script Python executado com sucesso: ${stdout}`);
  });
};

// Atualizar o JSON a cada 10 segundos
setInterval(updateData, 10000);