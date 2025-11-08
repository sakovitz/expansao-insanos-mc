# Runbook: API de Geração de Comunicados

**Serviço**: Comunicado Image Generation API
**Versão**: 1.0.0
**Mantenedor**: Área de Expansão - Insanos MC
**Última atualização**: 2025-11-08

---

## 📋 Visão Geral

Este runbook documenta procedimentos operacionais para a API de geração de comunicados em imagem.

**Endpoints**:
- `POST /gerar-comunicado` - Gera imagem de comunicado
- `GET /health` - Health check
- `GET /` - Informações da API

**Tecnologias**:
- Python 3.11
- FastAPI 0.115.x
- Uvicorn 0.32.x
- Pillow 12.0.0

---

## 🚀 Inicialização

### Desenvolvimento

```bash
# 1. Ativar ambiente virtual
cd c:\Users\jonas\github\expansao-insanos-mc
expansao\Scripts\activate

# 2. Verificar dependências instaladas
pip list | grep -E "fastapi|uvicorn|pillow|pydantic"

# 3. Iniciar servidor
uvicorn automacoes.comunicado_imagem.api:app --reload --host 0.0.0.0 --port 8000

# 4. Verificar logs
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

### Produção

```bash
# 1. Instalar Gunicorn (production server)
pip install gunicorn

# 2. Iniciar com múltiplos workers
gunicorn automacoes.comunicado_imagem.api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log

# 3. Configurar como serviço systemd (Linux)
# Ver seção "Configuração de Serviço" abaixo
```

---

## 🔍 Monitoramento

### Health Check

```bash
# Verificar se API está respondendo
curl http://localhost:8000/health

# Resposta esperada
{"status":"healthy","service":"comunicado-api"}

# Se não responder em 5 segundos: ALERTA
```

### Métricas de Performance

**SLA**:
- Tempo de resposta: < 10 segundos (meta: < 2 segundos)
- Disponibilidade: > 99%
- Taxa de erro: < 1%

**Monitorar**:
```bash
# 1. Tempo médio de geração (logs)
grep "Comunicado gerado com sucesso" logs/api.log | awk '{print $NF}' | sed 's/ms//' | awk '{sum+=$1; count++} END {print sum/count "ms"}'

# 2. Taxa de erro
grep "ERROR" logs/api.log | wc -l

# 3. Uso de disco (outputs/)
du -sh automacoes/outputs/
```

---

## 🚨 Troubleshooting

### 1. API não inicia

**Sintomas**:
```
ModuleNotFoundError: No module named 'automacoes'
```

**Diagnóstico**:
```bash
# Verificar se está no diretório correto
pwd
# Deve ser: c:\Users\jonas\github\expansao-insanos-mc

# Verificar Python path
python -c "import sys; print(sys.path)"
```

**Solução**:
```bash
# Adicionar diretório ao PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH
# Ou no Windows:
set PYTHONPATH=%cd%;%PYTHONPATH%
```

---

### 2. Erro: "Fonte não encontrada"

**Sintomas**:
```json
{"detail": "Erro ao gerar imagem: Fonte não encontrada: ..."}
```

**Diagnóstico**:
```bash
# Verificar se fontes existem
ls automacoes/comunicado_imagem/templates/fonts/
# Deve listar: DejaVuSans-Bold.ttf, DejaVuSans.ttf
```

**Solução**:
```bash
# Baixar fontes
python download_fonts.py

# Ou manualmente
# 1. Acessar: https://sourceforge.net/projects/dejavu/
# 2. Baixar dejavu-fonts-ttf-2.37.zip
# 3. Extrair DejaVuSans-Bold.ttf e DejaVuSans.ttf
# 4. Copiar para automacoes/comunicado_imagem/templates/fonts/
```

---

### 3. Erro: "Texto muito longo"

**Sintomas**:
```json
{"detail": "Texto muito longo para caber na imagem..."}
```

**Diagnóstico**:
- Campo de entrada excede 100 caracteres
- Fonte mínima (30px) ainda não comporta o texto

**Solução**:
```bash
# Opção A: Reduzir texto de entrada
# Ex: "CONCLUSÃO DE ESTÁGIO PROBATÓRIO" → "CONCLUSÃO DE ESTÁGIO"

# Opção B: Ajustar tamanho mínimo de fonte (código)
# Em generator.py, alterar min_size de 30 para 20
```

---

### 4. Performance degradada (> 10 segundos)

**Sintomas**:
```json
{"generation_time_ms": 12543.21}
```

**Diagnóstico**:
```bash
# 1. Verificar tamanho do template
ls -lh automacoes/comunicado_imagem/templates/base_template.png

# 2. Verificar uso de CPU/memória
top -p $(pgrep uvicorn)

# 3. Verificar disco
df -h
```

**Soluções**:
```bash
# 1. Redimensionar template (se > 2MB)
python -c "
from PIL import Image
img = Image.open('automacoes/comunicado_imagem/templates/base_template.png')
img = img.resize((1542, 1600), Image.Resampling.LANCZOS)
img.save('automacoes/comunicado_imagem/templates/base_template.png', optimize=True)
"

# 2. Aumentar workers (produção)
# gunicorn ... --workers 8

# 3. Limpar outputs/ antigos
find automacoes/outputs/ -name "*.jpeg" -mtime +30 -delete
```

---

### 5. Erro 400: Validação falhou

**Sintomas**:
```json
{
  "detail": [
    {
      "loc": ["body", "data"],
      "msg": "Data inválida. Formato esperado: DD/MM/AAAA",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Diagnóstico**:
- Formato de data incorreto (ex: "2025-11-04" em vez de "04/11/2025")
- Formato de nome incorreto (ex: "XANDECO 183" em vez de "XANDECO (183)")

**Solução**:
- Corrigir dados de entrada conforme especificação:
  - `data`: "DD/MM/AAAA"
  - `nome_integrante`: "NOME (NÚMERO)"

---

## 🔄 Manutenção

### Limpeza de Arquivos Antigos

```bash
# Limpar imagens com mais de 30 dias
find automacoes/outputs/ -name "*.jpeg" -mtime +30 -delete

# Limpar logs antigos
find logs/ -name "*.log" -mtime +60 -delete
```

### Rotação de Logs

```bash
# Configurar logrotate (Linux)
cat > /etc/logrotate.d/comunicado-api << EOF
/var/log/comunicado-api/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
EOF
```

### Backup

```bash
# Backup de templates e fontes (semanal)
tar -czf backup-comunicado-$(date +%Y%m%d).tar.gz \
  automacoes/comunicado_imagem/templates/ \
  automacoes/comunicado_imagem/*.py

# Mover para storage
mv backup-comunicado-*.tar.gz /backup/
```

---

## 🧪 Testes

### Teste Manual

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Gerar comunicado de teste
curl -X POST http://localhost:8000/gerar-comunicado \
  -H "Content-Type: application/json" \
  -d '{
    "origem": "EXPANSÃO",
    "evento": "TESTE",
    "nome_integrante": "TESTE (999)",
    "resultado": "APROVADO:",
    "localizacao": "TESTE",
    "grau": "GRAU I",
    "data": "08/11/2025"
  }'

# 3. Verificar imagem gerada
ls -lh automacoes/outputs/20251108_TESTE.jpeg
```

### Testes Automatizados

```bash
# Executar suite de testes
pytest tests/ -v

# Teste com cobertura
pytest tests/ --cov=automacoes.comunicado_imagem --cov-report=html

# Teste de carga (com locust - opcional)
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

---

## 🔐 Segurança

### Validação de Entrada

- ✅ Todos os campos são validados por Pydantic
- ✅ Comprimento máximo: 200 caracteres
- ✅ Formatos específicos (data, nome)
- ✅ Sem execução de código arbitrário

### Proteção contra DoS

```bash
# Limitar taxa de requisições (Nginx)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    location /gerar-comunicado {
        limit_req zone=api burst=20;
        proxy_pass http://localhost:8000;
    }
}
```

---

## 📊 Logs

### Estrutura de Logs

```
2025-11-08 17:00:51 - automacoes.comunicado_imagem.api - INFO - Recebida requisição para gerar comunicado: XANDECO (183)
2025-11-08 17:00:51 - automacoes.comunicado_imagem.validator - INFO - Data validada: 04/11/2025
2025-11-08 17:00:51 - automacoes.comunicado_imagem.generator - INFO - Nome de arquivo gerado: 20251104_XANDECO.jpeg
2025-11-08 17:00:51 - automacoes.comunicado_imagem.generator - INFO - Salvando imagem: automacoes/outputs/20251104_XANDECO.jpeg
2025-11-08 17:00:51 - automacoes.comunicado_imagem.api - INFO - Comunicado gerado com sucesso em 507.77ms: automacoes/outputs/20251104_XANDECO.jpeg
```

### Níveis de Log

- **INFO**: Operações normais
- **WARNING**: Situações suspeitas mas não críticas
- **ERROR**: Erros recuperáveis
- **CRITICAL**: Falhas críticas

### Monitoramento de Logs

```bash
# Tail em tempo real
tail -f logs/api.log

# Filtrar erros
grep ERROR logs/api.log

# Contar requisições por hora
grep "Recebida requisição" logs/api.log | cut -d' ' -f1-2 | uniq -c
```

---

## 📞 Contatos

**Escalonamento**:
1. **L1**: Verificar logs e executar procedimentos deste runbook
2. **L2**: Reiniciar serviço, verificar recursos do sistema
3. **L3**: Desenvolvedor (análise de código, debugging)

**Documentação adicional**:
- [README.md](../../automacoes/comunicado_imagem/README.md)
- [Especificação](../../specs/automacoes/001-comunicado-imagem/spec.md)
- [API Spec](../../specs/automacoes/001-comunicado-imagem/contracts/api-spec.yaml)

---

## 📝 Changelog

### v1.0.0 (2025-11-08)
- ✅ Implementação inicial
- ✅ Suporte UTF-8 completo
- ✅ 27 testes unitários e de integração
- ✅ Documentação completa
