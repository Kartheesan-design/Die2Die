module sram_die_top (
  input         clk0,
  input         csb0,
  input         web0,
  input  [3:0]  wmask0,
  input  [7:0]  addr0,
  input  [31:0] din0,
  output [31:0] dout0,
  input         clk1,
  input         csb1,
  input  [7:0]  addr1,
  output [31:0] dout1
);

  sky130_sram_1kbyte_1rw1r_32x256_8 sram_macro (
    .clk0   (clk0),
    .csb0   (csb0),
    .web0   (web0),
    .wmask0 (wmask0),
    .addr0  (addr0),
    .din0   (din0),
    .dout0  (dout0),
    .clk1   (clk1),
    .csb1   (csb1),
    .addr1  (addr1),
    .dout1  (dout1)
  );

endmodule
