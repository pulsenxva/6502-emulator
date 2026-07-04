class CPU:
  def __init__(self):
    self.memory = [0]*65536

    self.a = 0x00
    self.x = 0x00
    self.y = 0x00
    self.pc = 0x1000

  def tick(self):
    command = self.memory[self.pc]
    #print(hex(self.pc), command)
    if command == 0xA9:
      self.LDA(0)
      self.pc += 2
    if command == 0xA2:
      self.LDX(0)
      self.pc += 2
    if command ==0xA0:
      self.LDY(0)
      self.pc += 2
    if command == 0x8D:
      self.STA(1)
      self.pc += 3
    if command == 0x8E:
      self.STX(1)
      self.pc += 3
    if command == 0x8C:
      self.STY(1)
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
  def STX(self, mode):
    lsb = self.memory[self.pc+1]
    msb = self.memory[self.pc+2]
    loc = msb*256 + lsb
    self.memory[loc] = self.x
  def STY(self, mode):
    lsb = self.memory[self.pc+1]
    msb = self.memory[self.pc+2]
    loc = msb*256 + lsb
    self.memory[loc] = self.y

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

# STA 0x4400
cpu.memory[0x1006] = 0x8D
cpu.memory[0x1007] = 0x00
cpu.memory[0x1008] = 0x44

# STX 0x4401
cpu.memory[0x1009] = 0x8E
cpu.memory[0x100A] = 0x01
cpu.memory[0x100B] = 0x44

# STY 0x4402
cpu.memory[0x100C] = 0x8C
cpu.memory[0x100D] = 0x02
cpu.memory[0x100E] = 0x44

for _ in range(200): cpu.tick()

print("A", cpu.a)
print("B", cpu.x)
print("C", cpu.y)

print("STA", cpu.memory[0x4400])
print("STX", cpu.memory[0x4401])
print("STY", cpu.memory[0x4402])
