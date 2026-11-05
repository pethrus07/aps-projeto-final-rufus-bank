# Painéis internos (React com Vite)

SAC, antifraude e administração (RF025, RF027, RF030). Decisão: ADR-012. O build gera arquivos estáticos que a API serve em `/admin`, liberado só para os IPs da empresa (regra do WAF), com senha e TOTP.

Criado no Sprint 1 com:

```
npm create vite@latest . -- --template react-ts
```
