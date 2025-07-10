services:
  postgres:
    image: {{DH_ADDR}}/postgres:15-alpine
    restart: always
    environment:
      TZ: "Asia/Shanghai"
      POSTGRES_DB: "{{POSTGRES_DB}}"
      POSTGRES_USER: "{{POSTGRES_USER}}"
      POSTGRES_PASSWORD: "{{PASSWORD_POSTGRES}}"
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
      - ./postgres/initdb.d:/docker-entrypoint-initdb.d
    ports:
      - "{{PORT_POSTGRES}}:5432/tcp"
    networks:
      - shenma

networks:
  shenma:
    driver: bridge

