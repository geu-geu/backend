import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Create dummy users
  for (const username of ['alice', 'bob', 'charlie']) {
    const email = `${username}@example.com`;
    const password = 'password';
    const user = await prisma.user.upsert({
      where: { email },
      update: {},
      create: { email, password },
    });
    console.log(user);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
