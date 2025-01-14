import { ArgumentsHost, Catch, HttpStatus } from '@nestjs/common';
import { BaseExceptionFilter } from '@nestjs/core';
import { Prisma } from '@prisma/client';
import { Response } from 'express';

@Catch(Prisma.PrismaClientKnownRequestError)
export class PrismaClientExceptionFilter extends BaseExceptionFilter {
  catch(exception: Prisma.PrismaClientKnownRequestError, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse<Response>();

    switch (exception.code) {
      case 'P2002': {
        const status = HttpStatus.CONFLICT;
        const properties = exception.meta?.target;
        response.status(status).json({
          statusCode: status,
          message: `Unique constraint failed on ${properties}`,
        });
        break;
      }
      case 'P2025': {
        const status = HttpStatus.NOT_FOUND;
        response.status(status).json({
          statusCode: status,
          message: 'Not Found',
        });
        break;
      }
      default: {
        super.catch(exception, host);
        break;
      }
    }
  }
}
