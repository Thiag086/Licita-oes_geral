# Suporte

## Como Obter Ajuda

### 📚 Documentação

- **README.md**: Guia completo de uso
- **CHANGELOG.md**: Histórico de mudanças
- **CONTRIBUTING.md**: Guia para contribuidores
- **Exemplos**: Veja `exemplo_uso.py`

### 🐛 Reportando Problemas

Se você encontrou um bug ou tem uma dúvida:

1. **Verifique** se já existe uma issue similar
2. **Crie** uma nova issue com:
   - Título descritivo
   - Descrição clara do problema
   - Passos para reproduzir
   - Informações do sistema
   - Logs de erro (se houver)

### 💡 Sugerindo Melhorias

Para sugerir novas funcionalidades:

1. **Verifique** se já existe uma sugestão similar
2. **Crie** uma issue com:
   - Título descritivo
   - Descrição da melhoria
   - Casos de uso
   - Benefícios esperados

### ❓ Perguntas Frequentes

#### Q: O script não está funcionando, o que fazer?
A: 
1. Verifique se o Python 3.8+ está instalado
2. Instale as dependências: `pip install -r requirements.txt`
3. Teste com dados de exemplo: `python main.py --exemplo`
4. Verifique sua conexão com a internet

#### Q: Como instalar o script?
A: 
```bash
git clone https://github.com/Thiag086/Licita-oes_geral.git
cd Licita-oes_geral
pip install -r requirements.txt
python main.py --help
```

#### Q: Posso usar o script comercialmente?
A: Sim! O projeto está sob licença MIT, permitindo uso comercial.

#### Q: Como contribuir com o projeto?
A: Veja o arquivo `CONTRIBUTING.md` para detalhes completos.

#### Q: O script está lento, como otimizar?
A: 
- Use filtros específicos para reduzir resultados
- Ajuste o tamanho da página com `--tamanho`
- Use `--metodo web` se a API estiver lenta

#### Q: Posso personalizar o script?
A: Sim! O código é aberto e você pode modificá-lo conforme necessário.

### 🔧 Solução de Problemas

#### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

#### Erro: "Permission denied"
```bash
chmod +x *.py
```

#### Erro: "Connection timeout"
- Verifique sua conexão com a internet
- Tente usar `--metodo web`
- Aumente o timeout nas configurações

#### Erro: "No data found"
- Verifique se os filtros estão corretos
- Tente usar `--exemplo` para testar
- Verifique se a API do PNCP está funcionando

### 📞 Contato

- **GitHub Issues**: [Abrir issue](../../issues)
- **Email**: [seu-email@exemplo.com]
- **Discord**: [Link do servidor]
- **Telegram**: [Link do grupo]

### 🕒 Horários de Suporte

- **Segunda a Sexta**: 9h às 18h (Brasil)
- **Finais de semana**: Resposta em até 48h

### 🌟 Apoie o Projeto

Se este projeto te ajudou:

- ⭐ Dê uma estrela no GitHub
- 🐛 Reporte bugs
- 💡 Sugira melhorias
- 🤝 Contribua com código
- 📢 Compartilhe com outros

### 📝 Logs e Debug

Para obter mais informações sobre erros:

```bash
python main.py --exemplo --excel debug.xlsx 2>&1 | tee debug.log
```

### 🔄 Atualizações

Para manter o projeto atualizado:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Obrigado por usar o Listador de Licitações PNCP!** 🎉