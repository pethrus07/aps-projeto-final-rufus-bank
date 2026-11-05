import { Module } from '@nestjs/common';

/**
 * Módulo notificacao. Push, SMS, voz (Polly com cache), lembretes e a tabela outbox lida pelo worker (ADR-008).
 * Esqueleto: controllers, casos de uso e repositórios entram a partir do Sprint 1.
 */
@Module({})
export class ModuloNotificacao {}
