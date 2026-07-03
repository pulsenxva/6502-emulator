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
    if command == 0xA2:
      self.LDX(0)
      self.pc+=2
    if command ==0xA0:
      self.LDY(0)
      self.pc+=2
    if command == 0x8D:
      self.STA(1)
      self.pc += 3

  def LDA(self, mode):
    val = self.memory[self.pc+1]
    self.a = val
  
  def LDX(self, mode):
    val = self.memory[self.pc+1]
    self.x = val

  def LDY(self, mode):
    val = self.memory[self.pc+1]
    self.y = val

  def STA(self, mode):
    lsb = self.memory[self.pc+1]
    msb = self.memory[self.pc+2]
    loc = msb*256 + lsb
    self.memory[loc] = self.a
    self.pc += 3

cpu = CPU()

# LDA
cpu.memory[0x1000] = 0xA9
cpu.memory[0x1001] = 0x44

# LDX
cpu.memory[0x1002] = 0xA2
cpu.memory[0x1003] = 0x45

# LDY
cpu.memory[0x1004] = 0xA0
cpu.memory[0x1005] = 0x46

# STA
cpu.memory[0x1006] = 0x8D
cpu.memory[0x1007] = 0x00
cpu.memory[0x1008] = 0x44

for _ in range(200): cpu.tick()

print(cpu.a)
print(cpu.x)
print(cpu.y)

print(cpu.memory[0x4400])
