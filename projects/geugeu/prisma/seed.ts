import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  // Create dummy users
  for (const username of ['alice', 'bob', 'charlie']) {
    const email = `${username}@example.com`;
    const password = await hashPassword('password');
    const user = await prisma.user.upsert({
      where: { email },
      update: { password },
      create: { email, password },
    });
    console.log(user);
  }
}

async function hashPassword(rawPassword: string): Promise<string> {
  return await bcrypt.hash(rawPassword, 10);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
