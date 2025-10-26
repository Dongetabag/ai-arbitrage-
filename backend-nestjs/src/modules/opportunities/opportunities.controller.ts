/**
 * Opportunities Controller - NestJS
 * RESTful endpoints for opportunity management
 */

import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { OpportunitiesService } from './opportunities.service';

@Controller('api/opportunities')
export class OpportunitiesController {
  constructor(private readonly opportunitiesService: OpportunitiesService) {}

  @Get()
  async findAll(
    @Query('category') category?: string,
    @Query('min_profit') minProfit?: number,
    @Query('limit') limit: number = 100,
  ) {
    return this.opportunitiesService.findAll({
      category,
      minProfit,
      limit,
    });
  }

  @Get(':id')
  async findOne(@Param('id') id: number) {
    return this.opportunitiesService.findOne(id);
  }

  @Post('scan')
  async triggerScan(@Body() scanRequest: any) {
    // Trigger background scan
    return this.opportunitiesService.triggerScan(scanRequest);
  }

  @Get('stats/summary')
  async getStats() {
    return this.opportunitiesService.getStatsSummary();
  }
}

