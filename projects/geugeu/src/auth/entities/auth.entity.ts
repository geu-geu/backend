import { ApiProperty } from '@nestjs/swagger';

export class AuthEntity {
  constructor(partial: Partial<AuthEntity>) {
    Object.assign(this, partial);
  }

  @ApiProperty()
  accessToken: string;
}
