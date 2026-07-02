class CPU:
  def __init__(self):
    self.memory = [0]*65536

    self.a = 0x00
    self.x = 0x00
    self.y = 0x00
    self.pc = 0x1000

  def tick(self):
    command = self.memory[self.pc]
    if command == 0xA9:
      self.LDA(0)
      self.pc+=2

  def LDA(self, mode):
    val = self.memory[self.pc+1]
    self.a = val

cpu = CPU()

print(cpu.a)

cpu.memory[0x1000] = 0xA9
cpu.memory[0x1001] = 0x44

cpu.tick()
print(cpu.a)
