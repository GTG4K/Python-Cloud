const armstrongNumbers: number[] = [];

function digitCount(n: number): number {
  const digitToString = n.toString();
  return digitToString.length;
}

function isArmstrong(n: number): boolean {
  const power = digitCount(n);
  let sum = 0;

  for (let value = n.toString(); value.length > 0; value = value.slice(0, -1)) {
    const digit = Number(value.at(-1));
    sum += digit ** power;
  }

  return sum === n;
}

for (let n = 9; n <= 9999; n += 1) {
  if (isArmstrong(n)) armstrongNumbers.push(n);
}

function sumRecursive(numbers: number[], index = 0): number {
  if (index >= numbers.length) return 0;
  return numbers[index] + sumRecursive(numbers, index + 1);
}

const total = sumRecursive(armstrongNumbers);
