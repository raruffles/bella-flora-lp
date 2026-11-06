# 🌿 Bella Flora Farmácia de Manipulação — Landing Page de Alta Conversão

Instância isolada, moderna e pronta para deploy direto na **Vercel**.

## 🚀 Como fazer o Deploy na Vercel

### Opção 1: Via Vercel CLI (Direto do Terminal)
Se você tiver a CLI da Vercel instalada, basta navegar até esta pasta e rodar:
```bash
cd c:\portfólio\Portfólio-site\bella-flora-lp
npx vercel
```
Para deploy imediato em produção:
```bash
npx vercel --prod
```

### Opção 2: Via GitHub + Dashboard Vercel
1. Crie um repositório no seu GitHub (ex: `bella-flora-lp`).
2. Suba o conteúdo desta pasta para a branch principal.
3. Acesse [vercel.com/new](https://vercel.com/new), selecione o repositório e clique em **Deploy**. (Como é HTML estático de alta performance com `vercel.json`, o deploy é instantâneo e sem necessidade de etapas de build pesadas).

---

## 🛠️ Como Testar Localmente

Você pode iniciar um servidor local rápido utilizando `serve`, `http-server` ou `vite`:
```bash
npx -y serve . -l 3000
# ou
npx -y http-server . -p 3000
```
Depois abra [http://localhost:3000](http://localhost:3000) no seu navegador.

---

## 📂 Estrutura dos Arquivos

```
bella-flora-lp/
├── index.html          # LP completa com HTML semântico, Tailwind CSS, microinterações e scripts
├── vercel.json         # Configuração oficial da Vercel (clean URLs, headers de segurança, cache)
├── package.json        # Metadados do projeto e scripts npm
├── README.md           # Este guia de execução e deploy
└── imgs/               # Ativos visuais em alta resolução
    ├── logo.png                # Logotipo oficial da Bella Flora
    ├── hero-pharmacist.jpg     # Foto do time farmacêutico e prescrições
    ├── lab-sterile.jpg         # Laboratório moderno com cabine estéril
    ├── capsules-magistral.jpg  # Cápsulas magistrais sob medida
    ├── skincare-serum.jpg      # Dermocosméticos e séruns com conta-gotas
    ├── vitamins-supplements.jpg# Suplementos esportivos e vitaminas
    ├── herbal-phytotherapy.jpg # Fitoterápicos e ervas medicinais
    └── pharmacist-team.jpg     # Análise de fórmulas farmacêuticas
```

---

## 💎 Recursos de Conversão e UX Implementados

1. **Simulador / Calculadora Interativa de Receita:** Gera mensagens personalizadas pré-formatadas para o WhatsApp com nome, tipo de fórmula, tempo de tratamento e preferência de entrega.
2. **Plantão Ativo & Alerta Superior:** Notificação visual de que os farmacêuticos estão online respondendo até as 20h.
3. **Barra Fixa Mobile Inferior:** Botão de WhatsApp de fácil alcance com o polegar em dispositivos móveis, sem obstruir o conteúdo.
4. **Notificação de Prova Social Flutuante (Toast):** Simulação dinâmica e elegante de receitas e orçamentos recentes atendidos na região.
5. **Especialidades com Fotos Reais:** 6 cards detalhados com imagens de alta definição e botões de orçamento dedicados.
6. **Comparativo Transparente:** Tabela detalhando por que manipular na Bella Flora é superior a comprar caixas convencionais de drogaria.
7. **Compliance Sanitário Total:** Schema.org `Pharmacy`, avisos regulatórios da ANVISA RDC 67/2007 e RDC 44/2009 e CRF-SP.
