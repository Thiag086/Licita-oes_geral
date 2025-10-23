# Guia de Contribuição

Obrigado por considerar contribuir para o Listador de Licitações PNCP! 

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor:

1. Verifique se o bug já foi reportado nas [Issues](../../issues)
2. Se não foi reportado, crie uma nova issue com:
   - Título descritivo
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. atual
   - Informações do sistema (OS, versão do Python, etc.)

### Sugerindo Melhorias

Para sugerir melhorias:

1. Verifique se a sugestão já existe nas [Issues](../../issues)
2. Crie uma nova issue com:
   - Título descritivo
   - Descrição clara da melhoria
   - Casos de uso
   - Benefícios esperados

### Contribuindo com Código

1. **Fork** o repositório
2. **Clone** seu fork localmente:
   ```bash
   git clone https://github.com/SEU_USUARIO/Licita-oes_geral.git
   cd Licita-oes_geral
   ```
3. **Crie** uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
4. **Instale** as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. **Faça** suas alterações
6. **Teste** suas alterações:
   ```bash
   python main.py --exemplo
   python main.py --help
   ```
7. **Commit** suas alterações:
   ```bash
   git add .
   git commit -m "Adiciona nova funcionalidade"
   ```
8. **Push** para sua branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```
9. **Abra** um Pull Request

## Padrões de Código

### Python

- Siga o [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use docstrings para funções e classes
- Mantenha linhas com no máximo 127 caracteres
- Use type hints quando apropriado

### Commits

- Use mensagens de commit descritivas
- Use o formato: `tipo: descrição breve`
- Exemplos:
  - `feat: adiciona suporte a filtro por data`
  - `fix: corrige erro de formatação de data`
  - `docs: atualiza README com novos exemplos`

### Testes

- Adicione testes para novas funcionalidades
- Mantenha cobertura de testes alta
- Teste casos de erro e edge cases

## Estrutura do Projeto

```
├── main.py                 # Script principal
├── pncp_licitacoes.py     # Cliente para API do PNCP
├── pncp_web_scraper.py    # Web scraper para PNCP
├── exemplo_uso.py         # Exemplos de uso
├── config.py              # Configurações
├── requirements.txt       # Dependências
├── README.md              # Documentação principal
├── LICENSE                # Licença MIT
└── CHANGELOG.md           # Histórico de mudanças
```

## Processo de Review

1. **Automático**: GitHub Actions executa testes e linting
2. **Manual**: Mantenedores revisam o código
3. **Feedback**: Sugestões de melhoria são fornecidas
4. **Aprovação**: Pull Request é aprovado e mergeado

## Dúvidas?

Se você tem dúvidas sobre como contribuir:

1. Abra uma [Issue](../../issues) com a tag `question`
2. Consulte a [documentação](../../wiki)
3. Entre em contato com os mantenedores

## Agradecimentos

Obrigado por contribuir para tornar este projeto melhor! 🎉