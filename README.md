# LingoTutor (Streamlit)

Um “mini Duolingo” em Streamlit para estudar Inglês e Espanhol. Tem currículo fixo (6 lições por nível), exercícios `select` e `arrange`, geração on‑the‑fly de exercícios via Gemini e tutor em chat.

## Requisitos
- Python 3.10+
- Dependências (já listadas em `requirements.txt`):
  - `streamlit`
  - `google-generativeai`

## Instalação e execução local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como obter sua API Key do Gemini

Para que o LingoTutor funcione corretamente, é necessário gerar uma **API Key do Google Gemini**:

1. Acesse: [https://aistudio.google.com/app/api-keys](https://aistudio.google.com/app/api-keys)
2. Clique em **Create API key** (Criar chave de API).
3. Copie a **chave gerada**.
4. Guarde essa chave com segurança (ela será usada na configuração do app).

## Configuração da API (Gemini)

Após obter a API Key, configure-a no LingoTutor usando **uma das opções abaixo** (nessa ordem de preferência):

1. **Streamlit Secrets**

   ```python
   st.secrets["GEMINI_API_KEY"]
   ```

2. **Variável de ambiente**

   ```bash
   export GEMINI_API_KEY="sua_api_key_aqui"
   ```

   (no Windows PowerShell)

   ```powershell
   setx GEMINI_API_KEY "sua_api_key_aqui"
   ```

3. **Campo na Sidebar do app**

   * Cole a chave manualmente no campo **“Gemini API Key”** exibido na barra lateral.

## Como usar
1) Abra o app, escolha idioma (Inglês/Espanhol) e clique em **Começar**.
2) Dashboard mostra as lições por nível (6 por nível). O primeiro de cada nível já vem desbloqueado.
3) Clique na lição para entrar nos exercícios. Tipos:
   - `select`: múltipla escolha.
   - `arrange`: montar frase clicando nas palavras.
4) **Prática Mágica** (no dashboard ou sidebar) chama a Gemini para gerar 3 exercícios novos instantaneamente.
5) **Tutor IA**: chat fixo no rodapé, com histórico por idioma. Use a sidebar para alternar idioma a qualquer momento.
6) XP é somado ao concluir lições. O app guarda progresso em `st.session_state`.

## Dicas de deploy (Streamlit Community)
1) Suba o repo com `requirements.txt`.
2) No painel do Streamlit Cloud, adicione o secret `GEMINI_API_KEY` (e opcional `GEMINI_MODEL`).
3) Faça o deploy; não precisa alterar código.

## Estrutura de dados
- `CURRICULUM` hardcoded com níveis Básico/Intermediário/Avançado para Inglês e Espanhol.
- Cada lição tem: id, título, descrição, ícone numérico, e 3 exercícios (`select` ou `arrange`).

## Observações de UI/UX
- Barra de chat fixa no rodapé, centralizada e responsiva.
- Sidebar personalizada com navegação (Dashboard, Tutor IA, Prática Mágica) e card de status (idioma + XP).
- Menu/rodapé padrão do Streamlit ocultos via CSS.
