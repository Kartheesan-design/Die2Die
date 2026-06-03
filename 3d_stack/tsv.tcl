# TSV placement for picorv32 (Die-1) + SRAM (Die-2)
# Load picorv32 die
set block [ord::get_db_block]
set units [$block getDefUnits]

# Place bonding pads in the 520-600um strip (empty zone)
# TSV pitch: 10um, size: 2x2um on met5
define_pin_shape_pattern \
    -layer met5 \
    -region {10 520 590 598} \
    -size {2.0 2.0} \
    -x_step 10 \
    -y_step 10

# Group TSV connections by function
# Clock
set_io_pin_constraint \
    -region "up:{10 520 50 598}" \
    -pin_names {clk}

# Memory control signals
set_io_pin_constraint \
    -region "up:{50 520 150 598}" \
    -pin_names {mem_valid mem_ready mem_wstrb[0] mem_wstrb[1] mem_wstrb[2] mem_wstrb[3]}

# Address bus
set_io_pin_constraint \
    -region "up:{150 520 300 598}" \
    -pin_names {mem_addr[0] mem_addr[1] mem_addr[2] mem_addr[3] mem_addr[4] mem_addr[5] mem_addr[6] mem_addr[7]}

# Write data bus
set_io_pin_constraint \
    -region "up:{300 520 450 598}" \
    -pin_names {mem_wdata[0] mem_wdata[1] mem_wdata[2] mem_wdata[3] mem_wdata[4] mem_wdata[5] mem_wdata[6] mem_wdata[7] mem_wdata[8] mem_wdata[9] mem_wdata[10] mem_wdata[11] mem_wdata[12] mem_wdata[13] mem_wdata[14] mem_wdata[15] mem_wdata[16] mem_wdata[17] mem_wdata[18] mem_wdata[19] mem_wdata[20] mem_wdata[21] mem_wdata[22] mem_wdata[23] mem_wdata[24] mem_wdata[25] mem_wdata[26] mem_wdata[27] mem_wdata[28] mem_wdata[29] mem_wdata[30] mem_wdata[31]}

# Read data bus
set_io_pin_constraint \
    -region "up:{450 520 590 598}" \
    -pin_names {mem_rdata[0] mem_rdata[1] mem_rdata[2] mem_rdata[3] mem_rdata[4] mem_rdata[5] mem_rdata[6] mem_rdata[7] mem_rdata[8] mem_rdata[9] mem_rdata[10] mem_rdata[11] mem_rdata[12] mem_rdata[13] mem_rdata[14] mem_rdata[15] mem_rdata[16] mem_rdata[17] mem_rdata[18] mem_rdata[19] mem_rdata[20] mem_rdata[21] mem_rdata[22] mem_rdata[23] mem_rdata[24] mem_rdata[25] mem_rdata[26] mem_rdata[27] mem_rdata[28] mem_rdata[29] mem_rdata[30] mem_rdata[31]}

place_pins -hor_layers met5 -ver_layers met4
