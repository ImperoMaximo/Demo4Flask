FROM node:20-alpine

WORKDIR /app

# Le contexte est la racine, donc on précise le chemin
COPY D4F_front/package*.json ./

RUN npm install

COPY D4F_front/ .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]