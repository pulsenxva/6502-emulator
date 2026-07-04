from enum import Enum, auto

class Mode(Enum):
  IMMEDIATE = auto()
  ABSOLUTE = auto()
  IMPLIED = auto()

class CPU:
  def __init__(self):
    self.memory = [0]*65536

    self.a = 0x00
    self.x = 0x00
    self.y = 0x00
    self.pc = 0x1000
    
    self.commands = {
      0xA9: {"func": self.LDA, "mode": Mode.IMMEDIATE},
      0xA2: {"func": self.LDX, "mode": Mode.IMMEDIATE},
      0xA0: {"func": self.LDY, "mode": Mode.IMMEDIATE},
      0x8D: {"func": self.STA, "mode": Mode.ABSOLUTE},
      0x8E: {"func": self.STX, "mode": Mode.ABSOLUTE},
      0x8C: {"func": self.STY, "mode": Mode.ABSOLUTE},
      0xE8: {"func": self.INX, "mode": Mode.IMPLIED},
      0xC8: {"func": self.INY, "mode": Mode.IMPLIED},
      0xCA: {"func": self.DEX, "mode": Mode.IMPLIED},
      0x88: {"func": self.DEY, "mode": Mode.IMPLIED},
      0xAA: {"func": self.TAX, "mode": Mode.IMPLIED},
      0xA8: {"func": self.TAY, "mode": Mode.IMPLIED},
      0x8A: {"func": self.TXA, "mode": Mode.IMPLIED},
      0x98: {"func": self.TYA, "mode": Mode.IMPLIED},
    } 

    self.increments = {
      Mode.IMMEDIATE: 2,
      Mode.ABSOLUTE: 3,
      Mode.IMPLIED: 1,
    }

  def tick(self):
    command = self.memory[self.pc]
    #print(hex(self.pc), command)
    
    if command in self.commands:
      func = self.commands[command]["func"]
      mode = self.commands[command]["mode"]
      func(mode)
      self.pc += self.increments[mode]
    else: self.pc += 1

  def get_location(self, mode):
    loc = 0
    if mode == Mode.IMMEDIATE: 
      loc = self.pc+1
    elif mode == Mode.ABSOLUTE:
      lsb = self.memory[self.pc+1]
      msb = self.memory[self.pc+2]
      loc = msb*256 + lsb
    return loc

  def LDA(self, mode):
    loc = self.get_location(mode)
    val = self.memory[loc]
    self.a = val
  def LDX(self, mode):
    loc = self.get_location(mode)
    val = self.memory[loc]
    self.x = val
  def LDY(self, mode):
    loc = self.get_location(mode)
    val = self.memory[loc]
    self.y = val

  def STA(self, mode):
    loc = self.get_location(mode)
    self.memory[loc] = self.a
  def STX(self, mode):
    loc = self.get_location(mode)
    self.memory[loc] = self.x
  def STY(self, mode):
    loc = self.get_location(mode)
    self.memory[loc] = self.y

  def INX(self, mode):
    self.x+=1
  def INY(self, mode):
    self.y+=1
  def DEX(self, mode):
    self.x-=1
  def DEY(self, mode):
    self.y-=1

  def TAX(self, mode):
    self.x = self.a
  def TAY(self, mode):
    self.y = self.a
  def TXA(self, mode):
    self.a = self.x
  def TYA(self, mode):
    self.a = self.y

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
print("X", cpu.x)
print("Y", cpu.y)

print("STA", cpu.memory[0x4400])
print("STX", cpu.memory[0x4401])
print("STY", cpu.memory[0x4402])

