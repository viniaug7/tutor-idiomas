import json
import os
import random
from datetime import date

import streamlit as st

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - dependency is optional at runtime
    genai = None


APP_NAME = "LingoTutor"
LANG_FLAGS = {"Inglês": "🇺🇸", "Espanhol": "🇪🇸"}
XP_PER_EXERCISE = 10


CURRICULUM = {
    "Inglês": {
        "Básico": [
            {
                "id": "en-basic-1",
                "title": "Saudações",
                "icon": "👋",
                "description": "Cumprimente e se apresente.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'Bom dia' em inglês?",
                        "options": ["Good morning", "Good night", "See you later"],
                        "answer": "Good morning",
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Prazer em conhecer você'.",
                        "options": ["Nice to meet you", "See you soon", "Good luck"],
                        "answer": "Nice to meet you",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte a frase: Meu nome é Ana.",
                        "words": ["name", "is", "My", "Ana"],
                        "answer": ["My", "name", "is", "Ana"],
                    },
                ],
            },
            {
                "id": "en-basic-2",
                "title": "No café",
                "icon": "☕",
                "description": "Peça bebidas simples.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como pedir um café educadamente?",
                        "options": [
                            "I'd like a coffee, please.",
                            "Give me coffee.",
                            "Bring coffee now.",
                        ],
                        "answer": "I'd like a coffee, please.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Onde fica o banheiro?",
                        "words": ["the", "Where", "is", "bathroom", "?"],
                        "answer": ["Where", "is", "the", "bathroom", "?"],
                    },
                    {
                        "type": "select",
                        "prompt": "Selecione a resposta para 'Obrigado':",
                        "options": ["Thanks!", "Later", "Hello!"],
                        "answer": "Thanks!",
                    },
                ],
            },
            {
                "id": "en-basic-3",
                "title": "Apresentações",
                "icon": "🙋",
                "description": "Fale sobre você e pergunte o nome.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar o nome de alguém?",
                        "options": [
                            "What's your name?",
                            "Where are you?",
                            "How old are you?",
                        ],
                        "answer": "What's your name?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu sou do Brasil.",
                        "words": ["Brazil", "am", "I", "from"],
                        "answer": ["I", "am", "from", "Brazil"],
                    },
                    {
                        "type": "select",
                        "prompt": "Escolha a resposta para 'Nice to meet you'.",
                        "options": ["Nice to meet you too.", "Bye now.", "Good luck."],
                        "answer": "Nice to meet you too.",
                    },
                ],
            },
            {
                "id": "en-basic-4",
                "title": "Números",
                "icon": "🔢",
                "description": "Conte de 1 a 10 em situações simples.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'sete' em inglês?",
                        "options": ["seven", "six", "ten"],
                        "answer": "seven",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu tenho três gatos.",
                        "words": ["three", "have", "I", "cats"],
                        "answer": ["I", "have", "three", "cats"],
                    },
                    {
                        "type": "select",
                        "prompt": "Qual é a tradução de 'nine'?",
                        "options": ["nove", "cinco", "dez"],
                        "answer": "nove",
                    },
                ],
            },
            {
                "id": "en-basic-5",
                "title": "Cores",
                "icon": "🎨",
                "description": "Reconheça e fale cores básicas.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Qual cor é 'red'?",
                        "options": ["vermelho", "azul", "verde"],
                        "answer": "vermelho",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu gosto da cor azul.",
                        "words": ["blue", "color", "the", "like", "I"],
                        "answer": ["I", "like", "the", "color", "blue"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'yellow'.",
                        "options": ["amarelo", "cinza", "branco"],
                        "answer": "amarelo",
                    },
                ],
            },
            {
                "id": "en-basic-6",
                "title": "Família",
                "icon": "👨‍👩‍👧",
                "description": "Fale sobre membros da família.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'irmã' em inglês?",
                        "options": ["sister", "aunt", "mother"],
                        "answer": "sister",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Meu pai é médico.",
                        "words": ["is", "My", "father", "doctor", "a"],
                        "answer": ["My", "father", "is", "a", "doctor"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'grandmother'.",
                        "options": ["avó", "tio", "prima"],
                        "answer": "avó",
                    },
                ],
            },
        ],
        "Intermediário": [
            {
                "id": "en-inter-1",
                "title": "Aeroporto",
                "icon": "🛫",
                "description": "Pergunte e responda no aeroporto.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'balcão de check-in'?",
                        "options": ["Check-in counter", "Boarding gate", "Baggage claim"],
                        "answer": "Check-in counter",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu tenho uma mala de mão.",
                        "words": ["a", "carry-on", "bag", "have", "I", "."],
                        "answer": ["I", "have", "a", "carry-on", "bag", "."],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Qual é o portão de embarque?'.",
                        "options": [
                            "What's the boarding gate?",
                            "Where is the airplane?",
                            "How long is the flight?",
                        ],
                        "answer": "What's the boarding gate?",
                    },
                ],
            },
            {
                "id": "en-inter-2",
                "title": "Hotel",
                "icon": "🏨",
                "description": "Faça check-in e tire dúvidas.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Traduza 'Tenho uma reserva'.",
                        "options": [
                            "I have a reservation.",
                            "I need the receipt.",
                            "I lost my luggage.",
                        ],
                        "answer": "I have a reservation.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Preciso de mais toalhas, por favor.",
                        "words": ["more", "towels", "please", "I", "need", ","],
                        "answer": ["I", "need", "more", "towels", ",", "please"],
                    },
                    {
                        "type": "select",
                        "prompt": "Como perguntar pela senha do Wi-Fi?",
                        "options": [
                            "What's the Wi-Fi password?",
                            "Where is the Wi-Fi?",
                            "Do you sell Wi-Fi?",
                        ],
                        "answer": "What's the Wi-Fi password?",
                    },
                ],
            },
            {
                "id": "en-inter-3",
                "title": "Restaurante",
                "icon": "🍝",
                "description": "Faça pedidos detalhados e perguntas.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar se o prato é vegetariano?",
                        "options": [
                            "Is this dish vegetarian?",
                            "Where is the chef?",
                            "Do you like vegetables?",
                        ],
                        "answer": "Is this dish vegetarian?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu gostaria de reservar uma mesa para dois.",
                        "words": ["for", "table", "like", "two", "a", "would", "I", "to", "reserve"],
                        "answer": ["I", "would", "like", "to", "reserve", "a", "table", "for", "two"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Could we have the check, please?'.",
                        "options": [
                            "Poderíamos ter a conta, por favor?",
                            "Podemos trocar de mesa?",
                            "Tem Wi-Fi aqui?",
                        ],
                        "answer": "Poderíamos ter a conta, por favor?",
                    },
                ],
            },
            {
                "id": "en-inter-4",
                "title": "Compras",
                "icon": "🛍️",
                "description": "Negocie preços e peça tamanhos.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar outro tamanho?",
                        "options": [
                            "Do you have this in a different size?",
                            "Where is the cashier?",
                            "Can I get a discount?",
                        ],
                        "answer": "Do you have this in a different size?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Você tem esse modelo em preto?",
                        "words": ["this", "in", "black", "you", "Do", "have", "model"],
                        "answer": ["Do", "you", "have", "this", "model", "in", "black"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor frase para pedir desconto?",
                        "options": [
                            "Is there any discount available?",
                            "Give me a discount now.",
                            "How much is your salary?",
                        ],
                        "answer": "Is there any discount available?",
                    },
                ],
            },
            {
                "id": "en-inter-5",
                "title": "Transporte",
                "icon": "🚌",
                "description": "Use ônibus, metrô e táxi.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar o horário do próximo ônibus?",
                        "options": [
                            "What time is the next bus?",
                            "Where is the bus color?",
                            "Do you drive a bus?",
                        ],
                        "answer": "What time is the next bus?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Preciso de um táxi até o hotel.",
                        "words": ["to", "a", "Need", "hotel", "taxi", "the", "I"],
                        "answer": ["I", "Need", "a", "taxi", "to", "the", "hotel"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Where is the subway station?'.",
                        "options": [
                            "Onde fica a estação de metrô?",
                            "Quanto custa a passagem?",
                            "Você aceita cartão?",
                        ],
                        "answer": "Onde fica a estação de metrô?",
                    },
                ],
            },
            {
                "id": "en-inter-6",
                "title": "Consultório",
                "icon": "🩺",
                "description": "Explique sintomas e receba instruções.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer que está com dor de cabeça?",
                        "options": [
                            "I have a headache.",
                            "My head is breakfast.",
                            "I need a new head.",
                        ],
                        "answer": "I have a headache.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Estou tomando este remédio duas vezes ao dia.",
                        "words": ["a", "day", "taking", "twice", "I", "am", "this", "medicine"],
                        "answer": ["I", "am", "taking", "this", "medicine", "twice", "a", "day"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'You should rest and drink water'.",
                        "options": [
                            "Você deve descansar e beber água",
                            "Você deve correr agora",
                            "Você deve trabalhar mais",
                        ],
                        "answer": "Você deve descansar e beber água",
                    },
                ],
            },
        ],
        "Avançado": [
            {
                "id": "en-adv-1",
                "title": "Reunião",
                "icon": "💼",
                "description": "Use frases formais em reuniões.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Escolha a melhor forma de sugerir uma pausa.",
                        "options": [
                            "Shall we take a short break?",
                            "Stop talking now.",
                            "Let's end the meeting.",
                        ],
                        "answer": "Shall we take a short break?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Se eu soubesse, teria preparado slides.",
                        "words": ["known", "prepared", "If", "slides", "had", "I", "would", "have", "I", ","],
                        "answer": ["If", "I", "had", "known", ",", "I", "would", "have", "prepared", "slides"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Vamos retomar esse ponto mais tarde'.",
                        "options": [
                            "Let's revisit this point later.",
                            "Stop this conversation now.",
                            "We will cancel this topic.",
                        ],
                        "answer": "Let's revisit this point later.",
                    },
                ],
            }
            ,
            {
                "id": "en-adv-2",
                "title": "Apresentações",
                "icon": "📊",
                "description": "Estruture apresentações e pontos-chave.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Melhor forma de introduzir um gráfico?",
                        "options": [
                            "As we can see in this chart...",
                            "Look at this thing.",
                            "Here is a picture.",
                        ],
                        "answer": "As we can see in this chart...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Vamos passar para a próxima seção.",
                        "words": ["move", "next", "section", "to", "Let's", "the"],
                        "answer": ["Let's", "move", "to", "the", "next", "section"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Let's keep this slide brief'.",
                        "options": [
                            "Vamos manter este slide breve.",
                            "Vamos pular este slide.",
                            "Vamos imprimir este slide.",
                        ],
                        "answer": "Vamos manter este slide breve.",
                    },
                ],
            },
            {
                "id": "en-adv-3",
                "title": "Negociação",
                "icon": "🤝",
                "description": "Negocie prazos e condições.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como propor um prazo mais longo?",
                        "options": [
                            "Could we extend the deadline by a week?",
                            "Give me more time now.",
                            "Do you like deadlines?",
                        ],
                        "answer": "Could we extend the deadline by a week?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Podemos discutir um desconto maior?",
                        "words": ["a", "discount", "We", "larger", "discuss", "can", "?"],
                        "answer": ["We", "can", "discuss", "a", "larger", "discount", "?"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor frase para encerrar negociação cordialmente:",
                        "options": [
                            "Let's revisit this tomorrow with fresh numbers.",
                            "We are done. Bye.",
                            "No deal, forget it.",
                        ],
                        "answer": "Let's revisit this tomorrow with fresh numbers.",
                    },
                ],
            },
            {
                "id": "en-adv-4",
                "title": "Feedback",
                "icon": "📝",
                "description": "Dê e receba feedback construtivo.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como suavizar uma crítica?",
                        "options": [
                            "One area we could improve is...",
                            "This is terrible.",
                            "You failed again.",
                        ],
                        "answer": "One area we could improve is...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Agradeço o retorno detalhado.",
                        "words": ["feedback", "the", "appreciate", "detailed", "I"],
                        "answer": ["I", "appreciate", "the", "detailed", "feedback"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Could you elaborate on that point?'.",
                        "options": [
                            "Você poderia detalhar esse ponto?",
                            "Você pode repetir isso rápido?",
                            "Você pode falar mais baixo?",
                        ],
                        "answer": "Você poderia detalhar esse ponto?",
                    },
                ],
            },
            {
                "id": "en-adv-5",
                "title": "Entrevista",
                "icon": "🎤",
                "description": "Responda perguntas comportamentais.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como iniciar uma resposta STAR?",
                        "options": [
                            "In that situation, my task was...",
                            "I don't remember.",
                            "It was fine.",
                        ],
                        "answer": "In that situation, my task was...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: O resultado foi um aumento de 20% nas vendas.",
                        "words": ["The", "increase", "20%", "sales", "in", "was", "result", "an"],
                        "answer": ["The", "result", "was", "an", "increase", "of", "20%", "in", "sales"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor forma de falar sobre um erro:",
                        "options": [
                            "I learned from that mistake and improved my process.",
                            "It wasn't my fault.",
                            "I never make mistakes.",
                        ],
                        "answer": "I learned from that mistake and improved my process.",
                    },
                ],
            },
            {
                "id": "en-adv-6",
                "title": "Escrita formal",
                "icon": "✉️",
                "description": "Escreva e-mails formais e resumos.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como solicitar confirmação de recebimento?",
                        "options": [
                            "Please confirm receipt at your earliest convenience.",
                            "Did you get it?",
                            "Answer me now.",
                        ],
                        "answer": "Please confirm receipt at your earliest convenience.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Anexo segue o relatório solicitado.",
                        "words": ["report", "requested", "Attached", "is", "the"],
                        "answer": ["Attached", "is", "the", "requested", "report"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Looking forward to your response'.",
                        "options": [
                            "Aguardo seu retorno",
                            "Até mais",
                            "Aguarde minha resposta",
                        ],
                        "answer": "Aguardo seu retorno",
                    },
                ],
            },
        ],
    },
    "Espanhol": {
        "Básico": [
            {
                "id": "es-basic-1",
                "title": "Saludos",
                "icon": "🙋",
                "description": "Cumprimente e apresente-se.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'Boa tarde' em espanhol?",
                        "options": ["Buenas tardes", "Buenos días", "Buenas noches"],
                        "answer": "Buenas tardes",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Meu nome é Carla.",
                        "words": ["Carla", "es", "nombre", "Mi"],
                        "answer": ["Mi", "nombre", "es", "Carla"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Prazer em conhecê-lo'.",
                        "options": [
                            "Encantado de conocerte",
                            "Hasta pronto",
                            "Cuídate",
                        ],
                        "answer": "Encantado de conocerte",
                    },
                ],
            },
            {
                "id": "es-basic-2",
                "title": "Restaurante",
                "icon": "🍽️",
                "description": "Peça comida de forma cortês.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como pedir a conta?",
                        "options": [
                            "La cuenta, por favor.",
                            "El baño, por favor.",
                            "Otra mesa, por favor.",
                        ],
                        "answer": "La cuenta, por favor.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu gostaria de água sem gás.",
                        "words": ["agua", "sin", "gas", "me", "gustaría", "de"],
                        "answer": ["Me", "gustaría", "agua", "sin", "gas"],
                    },
                    {
                        "type": "select",
                        "prompt": "Escolha a tradução para 'obrigado'.",
                        "options": ["Gracias", "Perdón", "Hola"],
                        "answer": "Gracias",
                    },
                ],
            },
            {
                "id": "es-basic-3",
                "title": "Presentaciones",
                "icon": "👥",
                "description": "Apresente-se e pergunte nomes.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar 'Qual é o seu nome?'",
                        "options": [
                            "¿Cómo te llamas?",
                            "¿Dónde estás?",
                            "¿Qué hora es?",
                        ],
                        "answer": "¿Cómo te llamas?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Sou do Brasil.",
                        "words": ["Brasil", "soy", "de", "Yo"],
                        "answer": ["Yo", "soy", "de", "Brasil"],
                    },
                    {
                        "type": "select",
                        "prompt": "Resposta apropriada para 'Encantado de conocerte'.",
                        "options": ["Igualmente.", "Hasta mañana.", "No gracias."],
                        "answer": "Igualmente.",
                    },
                ],
            },
            {
                "id": "es-basic-4",
                "title": "Números",
                "icon": "🔢",
                "description": "Use números de 1 a 10.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'cinco' em espanhol?",
                        "options": ["cinco", "siete", "ocho"],
                        "answer": "cinco",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Tenho duas irmãs.",
                        "words": ["hermanas", "dos", "Tengo"],
                        "answer": ["Tengo", "dos", "hermanas"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'nueve'.",
                        "options": ["nove", "cinco", "quatro"],
                        "answer": "nove",
                    },
                ],
            },
            {
                "id": "es-basic-5",
                "title": "Colores",
                "icon": "🎨",
                "description": "Fale sobre cores comuns.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Qual é a tradução de 'rojo'?",
                        "options": ["vermelho", "azul", "preto"],
                        "answer": "vermelho",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Eu gosto da cor verde.",
                        "words": ["verde", "color", "me", "gusta", "el"],
                        "answer": ["Me", "gusta", "el", "color", "verde"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'amarillo'.",
                        "options": ["amarelo", "branco", "marrom"],
                        "answer": "amarelo",
                    },
                ],
            },
            {
                "id": "es-basic-6",
                "title": "Familia",
                "icon": "👨‍👩‍👧",
                "description": "Descreva sua família.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer 'irmão' em espanhol?",
                        "options": ["hermano", "tío", "primo"],
                        "answer": "hermano",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Minha mãe é professora.",
                        "words": ["profesora", "Mi", "es", "madre"],
                        "answer": ["Mi", "madre", "es", "profesora"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'abuelo'.",
                        "options": ["avô", "irmão", "sobrinho"],
                        "answer": "avô",
                    },
                ],
            },
        ],
        "Intermediário": [
            {
                "id": "es-inter-1",
                "title": "Hotel",
                "icon": "🏨",
                "description": "Check-in e dúvidas comuns.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Traduza 'Tenho uma reserva'.",
                        "options": [
                            "Tengo una reserva.",
                            "Necesito una cama.",
                            "Perdí mi pasaporte.",
                        ],
                        "answer": "Tengo una reserva.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: A que horas é o café da manhã?",
                        "words": ["el", "desayuno", "es", "¿A", "qué", "hora", "?"],
                        "answer": ["¿A", "qué", "hora", "es", "el", "desayuno", "?"],
                    },
                    {
                        "type": "select",
                        "prompt": "Como perguntar pela senha do Wi-Fi?",
                        "options": [
                            "¿Cuál es la contraseña del Wi-Fi?",
                            "¿Dónde está el Wi-Fi?",
                            "¿Vende Wi-Fi?",
                        ],
                        "answer": "¿Cuál es la contraseña del Wi-Fi?",
                    },
                ],
            },
            {
                "id": "es-inter-2",
                "title": "Passeio",
                "icon": "🗺️",
                "description": "Peça direções e informações.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Traduza 'Quanto custa a entrada?'.",
                        "options": [
                            "¿Cuánto cuesta la entrada?",
                            "¿Dónde está la entrada?",
                            "¿Puedo salir ahora?",
                        ],
                        "answer": "¿Cuánto cuesta la entrada?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Estou procurando a estação de metrô.",
                        "words": ["buscando", "estoy", "metro", "estación", "la", "de"],
                        "answer": ["Estoy", "buscando", "la", "estación", "de", "metro"],
                    },
                    {
                        "type": "select",
                        "prompt": "Escolha a melhor opção para pedir ajuda.",
                        "options": [
                            "¿Puedes ayudarme?",
                            "Necesito un taxi.",
                            "Hasta luego.",
                        ],
                        "answer": "¿Puedes ayudarme?",
                    },
                ],
            },
            {
                "id": "es-inter-3",
                "title": "Restaurante",
                "icon": "🍲",
                "description": "Peça pratos e tire dúvidas do cardápio.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar se o prato é picante?",
                        "options": [
                            "¿Es picante este plato?",
                            "¿Dónde está el picante?",
                            "¿Cuánto cuesta el picante?",
                        ],
                        "answer": "¿Es picante este plato?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Poderia trazer água sem gelo?",
                        "words": ["sin", "Podría", "agua", "traer", "hielo", "?"],
                        "answer": ["Podría", "traer", "agua", "sin", "hielo", "?"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'La cuenta, por favor'.",
                        "options": [
                            "A conta, por favor.",
                            "A sobremesa, por favor.",
                            "A água, por favor.",
                        ],
                        "answer": "A conta, por favor.",
                    },
                ],
            },
            {
                "id": "es-inter-4",
                "title": "Compras",
                "icon": "🛒",
                "description": "Peça tamanhos, preços e descontos.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar outro tamanho?",
                        "options": [
                            "¿Tiene otra talla?",
                            "¿Dónde está la talla?",
                            "¿Qué talla soy yo?",
                        ],
                        "answer": "¿Tiene otra talla?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Quanto custa este casaco?",
                        "words": ["cuesta", "este", "abrigo", "?", "¿Cuánto"],
                        "answer": ["¿Cuánto", "cuesta", "este", "abrigo", "?"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor frase para pedir desconto.",
                        "options": [
                            "¿Hay algún descuento disponible?",
                            "Dame descuento ahora.",
                            "No quiero pagar.",
                        ],
                        "answer": "¿Hay algún descuento disponible?",
                    },
                ],
            },
            {
                "id": "es-inter-5",
                "title": "Transporte",
                "icon": "🚇",
                "description": "Use metrô, ônibus e táxi.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como perguntar o horário do próximo metrô?",
                        "options": [
                            "¿A qué hora pasa el próximo metro?",
                            "¿Dónde compro um metrô?",
                            "¿Te gusta el metro?",
                        ],
                        "answer": "¿A qué hora pasa el próximo metro?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Preciso de um táxi até o aeroporto.",
                        "words": ["un", "Necesito", "taxi", "hasta", "aeropuerto", "el"],
                        "answer": ["Necesito", "un", "taxi", "hasta", "el", "aeropuerto"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza '¿Dónde se compra el billete?'.",
                        "options": [
                            "Onde se compra o bilhete?",
                            "Quanto custa a passagem?",
                            "Qual é a cor do bilhete?",
                        ],
                        "answer": "Onde se compra o bilhete?",
                    },
                ],
            },
            {
                "id": "es-inter-6",
                "title": "Saúde",
                "icon": "🏥",
                "description": "Descreva sintomas e entenda recomendações.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como dizer que está com febre?",
                        "options": [
                            "Tengo fiebre.",
                            "Tengo hambre.",
                            "Tengo prisa.",
                        ],
                        "answer": "Tengo fiebre.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Estou tomando este remédio três vezes ao dia.",
                        "words": ["veces", "al", "día", "este", "tomando", "Estoy", "medicamento", "tres"],
                        "answer": ["Estoy", "tomando", "este", "medicamento", "tres", "veces", "al", "día"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Debe descansar y tomar agua'.",
                        "options": [
                            "Você deve descansar e tomar água",
                            "Você deve correr",
                            "Você deve trabalhar",
                        ],
                        "answer": "Você deve descansar e tomar água",
                    },
                ],
            },
        ],
        "Avançado": [
            {
                "id": "es-adv-1",
                "title": "Negócios",
                "icon": "💼",
                "description": "Converse em reuniões formais.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Traduza 'Vamos analisar os resultados'.",
                        "options": [
                            "Vamos analizar los resultados.",
                            "Vamos cerrar el trato.",
                            "Vamos cancelar la reunión.",
                        ],
                        "answer": "Vamos analizar los resultados.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Se concordarmos, assinaremos hoje.",
                        "words": ["hoy", "firmaremos", "Si", "estamos", "de", "acuerdo", ","],
                        "answer": ["Si", "estamos", "de", "acuerdo", ",", "firmaremos", "hoy"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor frase para encerrar um e-mail?",
                        "options": [
                            "Quedo atento a sus comentarios.",
                            "No responda este correo.",
                            "No me llames más.",
                        ],
                        "answer": "Quedo atento a sus comentarios.",
                    },
                ],
            }
            ,
            {
                "id": "es-adv-2",
                "title": "Presentaciones",
                "icon": "📊",
                "description": "Estruture apresentações formais.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como introduzir um slide?",
                        "options": [
                            "Como pueden ver en esta diapositiva...",
                            "Mira isso.",
                            "Esto es algo.",
                        ],
                        "answer": "Como pueden ver en esta diapositiva...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Vamos passar ao próximo tema.",
                        "words": ["al", "tema", "pasar", "Vamos", "siguiente"],
                        "answer": ["Vamos", "pasar", "al", "siguiente", "tema"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Mantengamos este punto breve'.",
                        "options": [
                            "Mantenhamos este ponto breve.",
                            "Vamos pular este ponto.",
                            "Vamos alongar este ponto.",
                        ],
                        "answer": "Mantenhamos este ponto breve.",
                    },
                ],
            },
            {
                "id": "es-adv-3",
                "title": "Negociación",
                "icon": "🤝",
                "description": "Negocie prazos e condições.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como pedir extensão de prazo?",
                        "options": [
                            "¿Podemos extender el plazo una semana?",
                            "Dame mais tempo.",
                            "No quero prazo.",
                        ],
                        "answer": "¿Podemos extender el plazo una semana?",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Podemos revisar o desconto amanhã.",
                        "words": ["revisar", "Podemos", "descuento", "mañana", "el"],
                        "answer": ["Podemos", "revisar", "el", "descuento", "mañana"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor frase para encerrar negociação:",
                        "options": [
                            "Volvamos a hablar mañana con más datos.",
                            "Acabou. Tchau.",
                            "Nunca mais fale comigo.",
                        ],
                        "answer": "Volvamos a hablar mañana con más datos.",
                    },
                ],
            },
            {
                "id": "es-adv-4",
                "title": "Feedback",
                "icon": "📝",
                "description": "Dê devolutivas construtivas.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como suavizar uma crítica?",
                        "options": [
                            "Un área que podemos mejorar es...",
                            "Esto está muy mal.",
                            "No sirves.",
                        ],
                        "answer": "Un área que podemos mejorar es...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Obrigado pelo feedback detalhado.",
                        "words": ["Gracias", "detalle", "el", "feedback", "por"],
                        "answer": ["Gracias", "por", "el", "feedback", "detalle"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza '¿Podrías profundizar en ese punto?'.",
                        "options": [
                            "Você poderia detalhar esse ponto?",
                            "Você pode parar de falar?",
                            "Você pode gritar?",
                        ],
                        "answer": "Você poderia detalhar esse ponto?",
                    },
                ],
            },
            {
                "id": "es-adv-5",
                "title": "Entrevista",
                "icon": "🎤",
                "description": "Responda perguntas de forma estruturada.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como iniciar resposta STAR?",
                        "options": [
                            "En esa situación, mi tarea era...",
                            "No recuerdo.",
                            "No importa.",
                        ],
                        "answer": "En esa situación, mi tarea era...",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: O resultado foi reduzir custos em 15%.",
                        "words": ["resultó", "El", "en", "15%", "costos", "reducir"],
                        "answer": ["El", "resultado", "fue", "reducir", "costos", "en", "15%"],
                    },
                    {
                        "type": "select",
                        "prompt": "Melhor forma de falar sobre erro:",
                        "options": [
                            "Aprendí de ese error y mejoré mi proceso.",
                            "No fue culpa minha.",
                            "Nunca erro.",
                        ],
                        "answer": "Aprendí de ese error y mejoré mi proceso.",
                    },
                ],
            },
            {
                "id": "es-adv-6",
                "title": "Redacción formal",
                "icon": "✉️",
                "description": "Escreva e-mails formais e resumos.",
                "exercises": [
                    {
                        "type": "select",
                        "prompt": "Como pedir confirmação de recebimento?",
                        "options": [
                            "Por favor, confirma de recibido.",
                            "Recebeste?",
                            "Manda aí.",
                        ],
                        "answer": "Por favor, confirma de recibido.",
                    },
                    {
                        "type": "arrange",
                        "prompt": "Monte: Anexo o relatório solicitado.",
                        "words": ["solicitado", "Adjunto", "reporte", "el"],
                        "answer": ["Adjunto", "el", "reporte", "solicitado"],
                    },
                    {
                        "type": "select",
                        "prompt": "Traduza 'Quedo atento a tu respuesta'.",
                        "options": [
                            "Fico atento à sua resposta",
                            "Fico atento ao seu pagamento",
                            "Não responderei",
                        ],
                        "answer": "Fico atento à sua resposta",
                    },
                ],
            },
        ],
    },
}


def init_session_state() -> None:
    defaults = {
        "view": "intro",
        "language": None,
        "profiles": {},
        "chat_history": {},
        "current_lesson": None,
        "current_exercise_index": 0,
        "last_feedback": None,
        "arrange_pool": [],
        "arrange_answer": [],
        "api_key": None,
        "model_key": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_css() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="🦜", layout="wide")
    hide = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 2rem;}
        /* garante que o toggle da sidebar continue acessível */
        [data-testid="collapsedControl"] {opacity: 1; pointer-events: auto;}
        /* Sidebar tema escuro (versão anterior) com navegação aprimorada */
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: #e5e7eb;
            padding-top: 1rem;
            border-right: 1px solid #111827;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] h4, 
        [data-testid="stSidebar"] h5, 
        [data-testid="stSidebar"] h6, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label {
            color: #e5e7eb !important;
        }
        [data-testid="stSidebar"] .stTextInput input {
            background: #0b1220;
            color: #e5e7eb;
            border: 1px solid #1f2937;
            border-radius: 10px;
        }
        [data-testid="stSidebar"] .stButton button {
            width: 100%;
            text-align: center;
            background: #0f172a;
            color: #e5e7eb;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 0.65rem 0.9rem;
            font-weight: 600;
            box-shadow: none;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: #111827;
            border-color: #10b981;
        }
        [data-testid="stSidebar"] .stButton button:focus {
            background: #111827;
            border-color: #10b981;
            color: #e5e7eb;
        }
        /* cartão de status */
        .sidebar-card {
            background: #0b1220;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 0.9rem;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        }
        .sidebar-tag {
            display: inline-block;
            background: #10b981;
            color: #0b1220;
            padding: 0.15rem 0.5rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .sidebar-card p, .sidebar-card strong {
            color: #e5e7eb;
        }
        /* Botões principais (fora da sidebar) em verde */
        div.stButton > button {
            background: #10b981;
            color: #0b1220;
            border: none;
            border-radius: 10px;
            font-weight: 700;
        }
        div.stButton > button:hover {
            background: #34d399;
        }
        /* Cards de lições */
        .lesson-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            margin-bottom: 0.5rem;
            min-height: 230px;
            display: flex;
            flex-direction: column;
        }
        .lesson-head {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .lesson-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: #0f172a;
        }
        .lesson-title {
            font-weight: 700;
            color: #0f172a;
            font-size: 1rem;
        }
        .lesson-level {
            color: #6b7280;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .lesson-desc {
            color: #475569;
            margin: 0.65rem 0 0.5rem;
            font-size: 0.95rem;
            min-height: 48px;
        }
        .lesson-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 0.5rem;
            margin-top: auto;
        }
        .status-pill {
            display: inline-block;
            padding: 0.35rem 0.6rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.8rem;
        }
        .status-open { background: #e8fff4; color: #047857; border: 1px solid #10b981; }
        .status-locked { background: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }
        .status-done { background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe; }
        /* Opções de múltipla escolha: manter estilo padrão, só aumentar fonte */
        [data-testid="stRadio"] label {
            font-size: 1rem;
            color: #111827 !important;
        }
    </style>
    """
    st.markdown(hide, unsafe_allow_html=True)


def resolve_api_key() -> str | None:
    stored = st.session_state.get("api_key")
    if stored:
        return stored
    key = None
    # st.secrets pode não existir; proteger para evitar StreamlitSecretNotFoundError
    try:
        key = st.secrets.get("GEMINI_API_KEY")  # type: ignore[attr-defined]
    except Exception:
        key = None
    if not key and os.getenv("GEMINI_API_KEY"):
        key = os.getenv("GEMINI_API_KEY")
    if not key and st.session_state.get("user_api_key"):
        key = st.session_state["user_api_key"]
    if key:
        st.session_state["api_key"] = key
    return key


def ensure_gemini_model():
    key = resolve_api_key()
    if not key or genai is None:
        return None
    if st.session_state.get("model_key") != key or not st.session_state.get("gemini_model"):
        genai.configure(api_key=key)
        candidates = []
        env_model = os.getenv("GEMINI_MODEL")
        if env_model:
            candidates.append(env_model)
        candidates.extend(
            [
                "models/gemini-flash-latest",  # recomendação atual
                "gemini-flash-latest",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-pro",
            ]
        )
        model_instance = None
        for name in candidates:
            try:
                model_instance = genai.GenerativeModel(name)
                st.session_state["gemini_model_name"] = name
                break
            except Exception:
                continue
        st.session_state["gemini_model"] = model_instance
        st.session_state["model_key"] = key
    return st.session_state.get("gemini_model")


def sidebar_controls():
    with st.sidebar:
        st.markdown("### 🦜 LingoTutor")
        st.caption("Pratique idiomas com IA em um layout claro.")
        user_input = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("user_api_key", ""),
            placeholder="AIza...",
            help="Usada para Prática Mágica e Tutor IA.",
        )
        if user_input:
            st.session_state["user_api_key"] = user_input.strip()
        key = resolve_api_key()
        if genai is None:
            st.warning("Instale google-generativeai para usar os recursos de IA.")
        elif key:
            st.success("Gemini pronto para uso.")
        else:
            st.info("Informe a chave para liberar IA.")
        if st.session_state.get("language"):
            langs = list(CURRICULUM.keys())
            current_lang = st.session_state.get("language")
            selected_lang = st.selectbox(
                "Idioma de estudo",
                options=langs,
                index=langs.index(current_lang),
                key="sidebar-language",
            )
            if selected_lang != st.session_state.get("language"):
                st.session_state.language = selected_lang
                get_profile(selected_lang)
                if selected_lang not in st.session_state["chat_history"]:
                    st.session_state["chat_history"][selected_lang] = [
                        {
                            "role": "assistant",
                            "content": f"Olá! Sou seu tutor de {selected_lang}. Como posso ajudar hoje?",
                        }
                    ]
                st.session_state.current_lesson = None
                st.session_state.current_exercise_index = 0
                st.session_state.arrange_pool = []
                st.session_state.arrange_answer = []
                st.session_state.view = "dashboard"
                st.rerun()
            st.markdown("---")
            st.markdown("#### Navegação")
            st.button(
                "🏠 Dashboard",
                on_click=lambda: st.session_state.update(view="dashboard"),
                use_container_width=True,
            )
            st.button(
                "💬 Tutor IA",
                on_click=lambda: st.session_state.update(view="chat"),
                use_container_width=True,
            )
            st.button(
                "🚀 Prática Mágica",
                on_click=lambda: generate_magic_practice(st.session_state["language"]),
                use_container_width=True,
            )
            st.markdown("---")
            profile = get_profile(st.session_state["language"])
            st.markdown(
                f"""
                <div class="sidebar-card">
                    <div class="sidebar-tag">{LANG_FLAGS.get(st.session_state['language'], '')} {st.session_state['language']}</div>
                    <p style="margin-top:0.7rem; margin-bottom:0.3rem;"><strong>XP:</strong> {profile['xp']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def get_profile(language: str) -> dict:
    profiles = st.session_state["profiles"]
    if language not in profiles:
        profiles[language] = {
            "xp": 0,
            "completed_lessons": [],
        }
    return profiles[language]


def award_xp(profile: dict, amount: int) -> None:
    profile["xp"] += amount


def flatten_lessons(language: str):
    lessons = []
    for level, items in CURRICULUM[language].items():
        for lesson in items:
            lessons.append((level, lesson))
    return lessons


def is_unlocked(language: str, lesson_id: str, level: str) -> bool:
    """Libera o primeiro exercício de cada nível e mantém sequência dentro do nível."""
    profile = get_profile(language)
    lessons_in_level = CURRICULUM[language][level]
    ids = [l["id"] for l in lessons_in_level]
    if lesson_id not in ids:
        return False
    idx = ids.index(lesson_id)
    if idx == 0:
        return True  # primeiro de cada nível fica desbloqueado
    prev_id = ids[idx - 1]
    return prev_id in profile["completed_lessons"]


def start_lesson(lesson: dict, level: str, source: str = "curriculum") -> None:
    st.session_state.current_lesson = {
        "id": lesson["id"],
        "title": lesson["title"],
        "icon": lesson["icon"],
        "description": lesson["description"],
        "exercises": lesson["exercises"],
        "level": level,
        "source": source,
    }
    st.session_state.current_exercise_index = 0
    st.session_state.arrange_pool = []
    st.session_state.arrange_answer = []
    st.session_state.last_feedback = None
    st.session_state.view = "lesson"


def complete_lesson() -> None:
    lang = st.session_state.get("language")
    lesson = st.session_state.get("current_lesson")
    if not lang or not lesson:
        st.session_state.view = "dashboard"
        return
    profile = get_profile(lang)
    if lesson["source"] == "curriculum" and lesson["id"] not in profile["completed_lessons"]:
        profile["completed_lessons"].append(lesson["id"])
    xp_gain = XP_PER_EXERCISE * len(lesson["exercises"])
    award_xp(profile, xp_gain)
    st.session_state.last_feedback = ("success", f"Lição concluída! +{xp_gain} XP")
    st.session_state.current_lesson = None
    st.session_state.current_exercise_index = 0
    st.session_state.arrange_pool = []
    st.session_state.arrange_answer = []
    st.session_state.view = "dashboard"
    st.balloons()


def render_feedback():
    feedback = st.session_state.get("last_feedback")
    if feedback:
        status, message = feedback
        if status == "success":
            st.success(message)
        else:
            st.error(message)
        st.session_state.last_feedback = None


def handle_correct_answer():
    lesson = st.session_state.current_lesson
    st.session_state.last_feedback = ("success", "Resposta correta! 🎯")
    st.session_state.current_exercise_index += 1
    st.session_state.arrange_pool = []
    st.session_state.arrange_answer = []
    if st.session_state.current_exercise_index >= len(lesson["exercises"]):
        complete_lesson()
        st.rerun()
    else:
        st.rerun()


def render_select_exercise(exercise: dict):
    key_prefix = f"{st.session_state.current_lesson['id']}-{st.session_state.current_exercise_index}"
    with st.form(key=f"form-{key_prefix}"):
        st.markdown(f"**{exercise['prompt']}**")
        choice = st.radio(
            "Opções",
            options=exercise["options"],
            key=f"select-{key_prefix}",
            label_visibility="collapsed",
            index=None,
        )
        submitted = st.form_submit_button("Verificar", type="primary", use_container_width=True)
        if submitted:
            if choice is None:
                st.session_state.last_feedback = ("error", "Escolha uma opção antes de verificar.")
            elif choice == exercise["answer"]:
                handle_correct_answer()
            else:
                st.session_state.last_feedback = ("error", "Resposta incorreta. Tente novamente.")


def prepare_arrange_state(exercise: dict):
    expected_key = f"{st.session_state.current_lesson['id']}-{st.session_state.current_exercise_index}"
    if st.session_state.get("arrange_key") != expected_key:
        st.session_state.arrange_key = expected_key
        st.session_state.arrange_pool = exercise["words"].copy()
        random.shuffle(st.session_state.arrange_pool)
        st.session_state.arrange_answer = []


def render_arrange_exercise(exercise: dict):
    prepare_arrange_state(exercise)
    key_prefix = st.session_state.arrange_key
    st.write(exercise["prompt"])
    pool_cols = st.columns(len(st.session_state.arrange_pool) or 1)
    for idx, word in enumerate(st.session_state.arrange_pool):
        col = pool_cols[idx % len(pool_cols)]
        if col.button(word, key=f"pool-{key_prefix}-{idx}"):
            st.session_state.arrange_answer.append(word)
            st.session_state.arrange_pool.pop(idx)
            st.rerun()

    st.markdown("**Sua frase:**")
    phrase_cols = st.columns(max(len(st.session_state.arrange_answer), 1))
    for idx, word in enumerate(st.session_state.arrange_answer):
        col = phrase_cols[idx % len(phrase_cols)]
        if col.button(word, key=f"phrase-{key_prefix}-{idx}"):
            st.session_state.arrange_pool.append(word)
            st.session_state.arrange_answer.pop(idx)
            st.rerun()

    controls = st.columns(2)
    if controls[0].button("Resetar frase", key=f"reset-{key_prefix}"):
        st.session_state.arrange_pool = exercise["words"].copy()
        random.shuffle(st.session_state.arrange_pool)
        st.session_state.arrange_answer = []
        st.rerun()

    if controls[1].button("Verificar resposta", key=f"verify-{key_prefix}", type="primary"):
        if st.session_state.arrange_answer == exercise["answer"]:
            handle_correct_answer()
        else:
            st.session_state.last_feedback = (
                "error",
                "Quase! Verifique a ordem das palavras.",
            )


def render_intro():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"🦜 {APP_NAME}")
        st.subheader("Seu tutor de idiomas estilo Duolingo, agora em Streamlit.")
        language = st.selectbox("Escolha um idioma para praticar", list(CURRICULUM.keys()))
        if st.button("Começar"):
            st.session_state.language = language
            get_profile(language)
            if language not in st.session_state["chat_history"]:
                st.session_state["chat_history"][language] = [
                    {
                        "role": "assistant",
                        "content": f"Olá! Sou seu tutor de {language}. Como posso ajudar hoje?",
                    }
                ]
            st.session_state.view = "dashboard"
            st.rerun()


def render_top_bar(lang: str, profile: dict):
    col1, col2 = st.columns([1, 1])
    col1.metric("Idioma", f"{LANG_FLAGS.get(lang, '')} {lang}")
    col2.metric("XP", profile["xp"])


def render_lessons(lang: str, profile: dict):
    level_order = ["Básico", "Intermediário", "Avançado"]
    cols = st.columns(3)
    for col, level in zip(cols, level_order):
        lessons = CURRICULUM[lang].get(level, [])
        # garante até 6 slots por nível
        padded = lessons[:6] + [None] * max(0, 6 - len(lessons))
        with col:
            st.markdown(f"#### {level}")
            for idx, lesson in enumerate(padded):
                if lesson is None:
                    st.markdown(
                        f"""
                        <div class="lesson-card">
                            <div class="lesson-head">
                                <div class="lesson-icon">{idx + 1}</div>
                                <div>
                                    <div class="lesson-title">Em breve</div>
                                    <div class="lesson-level">Slot vazio</div>
                                </div>
                            </div>
                            <p class="lesson-desc">Novo conteúdo será adicionado aqui.</p>
                            <div class="lesson-footer">
                                <span class="status-pill status-locked">Bloqueada</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.button(
                        "Em breve",
                        key=f"placeholder-{level}-{idx}",
                        disabled=True,
                        use_container_width=True,
                    )
                    continue

                unlocked = is_unlocked(lang, lesson["id"], level)
                completed = lesson["id"] in profile["completed_lessons"]
                status_text = "Concluída" if completed else ("Disponível" if unlocked else "Bloqueada")
                status_class = "status-done" if completed else ("status-open" if unlocked else "status-locked")
                if completed:
                    start_label = "Rever lição"
                elif unlocked:
                    start_label = "Começar"
                else:
                    start_label = "Bloqueada"
                st.markdown(
                    f"""
                    <div class="lesson-card">
                        <div class="lesson-head">
                            <div class="lesson-icon">{idx + 1}</div>
                            <div>
                                <div class="lesson-title">{lesson['title']}</div>
                                <div class="lesson-level">{level}</div>
                            </div>
                        </div>
                        <p class="lesson-desc">{lesson['description']}</p>
                        <div class="lesson-footer">
                            <span class="status-pill {status_class}">{status_text}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    start_label,
                    key=f"start-{lesson['id']}",
                    disabled=not unlocked,
                    use_container_width=True,
                    on_click=start_lesson,
                    args=(lesson, level),
                )


def parse_ai_response(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {"select", "arrange"}:
            continue
        if "prompt" not in item or "answer" not in item:
            continue
        if item["type"] == "select" and "options" in item:
            normalized.append(
                {
                    "type": "select",
                    "prompt": item["prompt"],
                    "options": item["options"],
                    "answer": item["answer"],
                }
            )
        elif item["type"] == "arrange" and "words" in item:
            normalized.append(
                {
                    "type": "arrange",
                    "prompt": item["prompt"],
                    "words": item["words"],
                    "answer": item["answer"],
                }
            )
    return normalized or None


def generate_magic_practice(lang: str):
    model = ensure_gemini_model()
    if not model:
        st.error("Configure a API key e um modelo Gemini válido (ex: models/gemini-flash-latest) para usar a prática mágica.")
        return
    profile = get_profile(lang)
    prompt = f"""
    Gere 3 exercícios rápidos para alunos de {lang} no estilo Duolingo.
    Use apenas os tipos "select" e "arrange".
    Responda somente com JSON válido sem texto extra.
    Estrutura:
    [
      {{"type": "select", "prompt": "...", "options": ["A","B","C"], "answer": "A"}},
      {{"type": "arrange", "prompt": "...", "words": ["palavra1","palavra2"], "answer": ["palavra1","palavra2"]}}
    ]
    Priorize temas do nível atual e mantenha instruções curtas. O usuário tem {profile['xp']} XP.
    """
    with st.spinner("Gerando exercícios com Gemini..."):
        try:
            response = model.generate_content(prompt)
            exercises = parse_ai_response(response.text)
        except Exception as exc:  # pragma: no cover - rede/modelo externo
            st.error(f"Não foi possível gerar exercícios: {exc}")
            return
    if not exercises:
        st.error("Não entendi o retorno da IA. Tente novamente.")
        return
    lesson = {
        "id": f"ai-{random.randint(1000, 9999)}",
        "title": "Prática Mágica",
        "icon": "✨",
        "description": "Exercícios criados pela IA agora mesmo.",
        "exercises": exercises,
    }
    start_lesson(lesson, level="IA", source="ai")


def render_dashboard():
    lang = st.session_state.get("language")
    if not lang:
        st.session_state.view = "intro"
        return
    profile = get_profile(lang)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"{APP_NAME} · {LANG_FLAGS.get(lang, '')} {lang}")
        render_top_bar(lang, profile)
        render_feedback()
        st.markdown("### Prática rápida")
        magic_cols = st.columns([2, 1])
        magic_cols[0].write("Gere exercícios personalizados com IA.")
        magic_cols[1].button("✨ Prática Mágica", on_click=generate_magic_practice, args=(lang,))

        st.markdown("### Lições")
        render_lessons(lang, profile)

        st.markdown("### Tutor IA")
        st.button("Abrir chat com tutor", on_click=lambda: st.session_state.update(view="chat"))


def render_progress(lesson: dict):
    total = len(lesson["exercises"])
    idx = st.session_state.current_exercise_index
    st.progress(idx / total, text=f"Progresso: {idx}/{total}")


def render_lesson():
    lang = st.session_state.get("language")
    lesson = st.session_state.get("current_lesson")
    if not lang or not lesson:
        st.session_state.view = "dashboard"
        return
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"{lesson['icon']} {lesson['title']}")
        st.caption(f"{lesson['description']} · {lesson['level']}")
        render_progress(lesson)
        render_feedback()
        if st.button("Voltar ao dashboard"):
            st.session_state.view = "dashboard"
            return
        idx = st.session_state.current_exercise_index
        if idx >= len(lesson["exercises"]):
            complete_lesson()
            return
        exercise = lesson["exercises"][idx]
        if exercise["type"] == "select":
            render_select_exercise(exercise)
        elif exercise["type"] == "arrange":
            render_arrange_exercise(exercise)


def ask_tutor(prompt: str, lang: str) -> str:
    model = ensure_gemini_model()
    if not model:
        return "Configure a API key e defina um modelo Gemini válido (ex: models/gemini-flash-latest)."
    system = (
        f"Você é um tutor nativo de {lang}. "
        "Corrija suavemente erros, incentive e responda de forma curta."
    )
    try:
        response = model.generate_content(
            [
                {"role": "user", "parts": system},
                {"role": "user", "parts": prompt},
            ]
        )
        return response.text
    except Exception as exc:  # pragma: no cover - rede/modelo externo
        return f"Não consegui responder agora: {exc}"


def render_chat():
    lang = st.session_state.get("language")
    if not lang:
        st.session_state.view = "intro"
        return
    history = st.session_state["chat_history"].setdefault(
        lang,
        [
            {
                "role": "assistant",
                "content": f"Olá! Sou seu tutor de {lang}. Como posso ajudar hoje?",
            }
        ],
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"Tutor IA · {LANG_FLAGS.get(lang, '')} {lang}")
        st.caption("Converse com um professor nativo e receba correções gentis.")
        if st.button("Voltar ao dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()
            return
        for message in history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        user_input = st.chat_input("Digite sua mensagem")
        if user_input:
            history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            with st.spinner("Tutor digitando..."):
                reply = ask_tutor(user_input, lang)
            history.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)


def main():
    inject_css()
    init_session_state()
    sidebar_controls()
    view = st.session_state.view
    if view == "intro":
        render_intro()
    elif view == "dashboard":
        render_dashboard()
    elif view == "lesson":
        render_lesson()
    elif view == "chat":
        render_chat()
    else:
        render_intro()


if __name__ == "__main__":
    main()
