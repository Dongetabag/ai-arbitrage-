/**
 * NestJS App Module
 * Modular architecture for maintainability
 */

import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MongooseModule } from '@nestjs/mongoose';
import { BullModule } from '@nestjs/bull';

// Feature modules
import { OpportunitiesModule } from './modules/opportunities/opportunities.module';
import { PurchasingModule } from './modules/purchasing/purchasing.module';
import { ListingModule } from './modules/listing/listing.module';
import { SupportModule } from './modules/support/support.module';
import { CommunicationModule } from './modules/communication/communication.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';

@Module({
  imports: [
    // Configuration
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // PostgreSQL (TypeORM)
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT) || 5432,
      username: process.env.DB_USER || 'arbitrage_user',
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME || 'arbitrage_db',
      autoLoadEntities: true,
      synchronize: process.env.NODE_ENV !== 'production',
    }),

    // MongoDB (Mongoose)
    MongooseModule.forRoot(
      process.env.MONGODB_URI || 'mongodb://localhost:27017/arbitrage_db'
    ),

    // Bull Queue (Redis-based)
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379,
      },
    }),

    // Feature modules
    OpportunitiesModule,
    PurchasingModule,
    ListingModule,
    SupportModule,
    CommunicationModule,
    AnalyticsModule,
  ],
})
export class AppModule {}

