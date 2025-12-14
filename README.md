# LingoTutor (Streamlit)

Aplicativo estilo Duolingo para praticar Inglês e Espanhol diretamente no Streamlit, com exercícios fixos e geração de novos desafios via Gemini.

## Requisitos
- Python 3.10+
- Dependências: `streamlit`, `google-generativeai`

## Como rodar
```bash
pip install streamlit google-generativeai
streamlit run app.py
```

## Chave da API (Gemini)
- Preferência: defina `GEMINI_API_KEY` em variáveis de ambiente ou em `st.secrets["GEMINI_API_KEY"]`.
- Se não existir, use o campo "Gemini API Key" na sidebar do app.

## Funcionalidades
- Fluxo de lições com exercícios `select` e `arrange`, XP e streak persistidos em `session_state`.
- Botão **Prática Mágica** gera 3 novos exercícios via Gemini em JSON.
- Tutor IA com `st.chat_message` para correções suaves no idioma escolhido.
- Interface centralizada, barra superior com bandeira, XP e Dias de Ofensiva, e menu oculto via CSS.
