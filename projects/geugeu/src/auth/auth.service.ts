import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { JwtService } from '@nestjs/jwt';
import { AuthEntity } from './entities/auth.entity';

@Injectable()
export class AuthService {
  constructor(
    private readonly prismaService: PrismaService,
    private readonly jwtService: JwtService,
  ) {}

  async login(email: string, password: string): Promise<AuthEntity> {
    const user = await this.prismaService.user.findUnique({ where: { email } });
    if (!user) {
      throw new UnauthorizedException('Incorrect email or password');
    }
    if (user.password !== password) {
      throw new UnauthorizedException('Incorrect email or password');
    }
    const accessToken = this.jwtService.sign({ userId: user.id });
    return new AuthEntity({ accessToken });
  }
}
