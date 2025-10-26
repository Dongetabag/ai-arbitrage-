/**
 * Opportunities Module - NestJS
 * Modular architecture for maintainability
 */

import { Module } from '@nestjs/common';
import { BullModule } from '@nestjs/bull';
import { OpportunitiesController } from './opportunities.controller';
import { OpportunitiesService } from './opportunities.service';

@Module({
  imports: [
    BullModule.registerQueue({
      name: 'scanning',
    }),
  ],
  controllers: [OpportunitiesController],
  providers: [OpportunitiesService],
  exports: [OpportunitiesService],
})
export class OpportunitiesModule {}

