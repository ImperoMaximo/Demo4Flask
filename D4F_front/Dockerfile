FROM node:20-alpine

WORKDIR /app

# Le contexte est la racine, donc on précise le chemin
COPY D4F_front/package*.json ./

RUN npm install

COPY D4F_front/ .

ENV VITE_BACK_API_BASE_URL="https://d4f.local/backend"

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host"]