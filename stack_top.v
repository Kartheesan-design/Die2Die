module stack_top;

wire clk;

wire mem_valid;
wire mem_ready;

wire [3:0]  mem_wstrb;
wire [7:0]  mem_addr;

wire [31:0] mem_wdata;
wire [31:0] mem_rdata;

picorv32 cpu (
    .clk(clk),

    .mem_valid(mem_valid),
    .mem_ready(mem_ready),

    .mem_wstrb(mem_wstrb),
    .mem_addr(mem_addr),

    .mem_wdata(mem_wdata),
    .mem_rdata(mem_rdata)
);

sram_die_top sram (
    .clk0(clk),

    .csb0(mem_valid),
    .web0(mem_ready),

    .wmask0(mem_wstrb),
    .addr0(mem_addr),

    .din0(mem_wdata),
    .dout0(mem_rdata)
);

endmodule
