# 9.5 Definition of Done (DoD)

Um item só está **pronto** quando cumpre todos os itens que se aplicam a ele. Item que não cumpre volta para o backlog e não conta na velocidade do sprint.

## Código

- [ ] Código revisado e aprovado por pelo menos 1 pessoa que não escreveu. Mudança em identidade, contas ou pagamentos precisa da aprovação do Tech Lead.
- [ ] Segue o [guia de padrões de código](../bloco-8-dev/) e passa no lint sem aviso.
- [ ] Nenhum módulo acessa tabela de outro módulo (regra de dependência do ADR-001 no lint).
- [ ] Nenhum segredo, senha ou dado pessoal no código ou no log.

## Testes

- [ ] Testes de unidade das regras novas.
- [ ] Teste de integração com PostgreSQL real quando mexe com banco, razão contábil, outbox ou idempotência.
- [ ] Cobertura do módulo dentro da meta de [03-metas-de-cobertura.md](03-metas-de-cobertura.md).
- [ ] Todos os critérios de aceite da história testados, de preferência automatizados.
- [ ] Pipeline verde: lint, testes, build, varredura de segurança.

## Segurança

- [ ] **Nenhuma vulnerabilidade crítica ou alta** aberta em dependência ou imagem (RNF06).
- [ ] Rota nova protegida por autenticação e papel corretos, ou marcada como pública no OpenAPI com o motivo.
- [ ] Ação de funcionário gera registro de auditoria (RNF14).

## Contrato e documentação

- [ ] `openapi.yaml` atualizado e o teste de contrato passando.
- [ ] Migração de banco no padrão expandir e contrair, sem parar o sistema (Bloco 5).
- [ ] Dicionário de dados atualizado se houver coluna nova, com a marcação LGPD.
- [ ] README e `.env.example` atualizados se houver variável nova.

## Acessibilidade e linguagem (toda tela)

- [ ] Botão "Ouvir" funcionando e o áudio confere com o texto da tela.
- [ ] Todo elemento tocável tem rótulo para o TalkBack e o VoiceOver, área de toque de pelo menos 48 dp e contraste de pelo menos 4,5:1 (RNF09).
- [ ] Texto revisado pelo UX: frases curtas e sem jargão.
- [ ] A ação principal da tela cabe no limite de 3 toques depois do login, quando for uma das ações principais (RNF08).
- [ ] Testado em um Android de entrada real com 3 GB de RAM (RNF10).

## Aceite

- [ ] Funcionando em homologação, e não só no localhost.
- [ ] Demonstrado na Sprint Review e aceito pelo PO.
- [ ] Se a tela é nova, passou no teste de uso do sprint com pessoas do perfil das personas, ou o problema encontrado virou item no backlog.
