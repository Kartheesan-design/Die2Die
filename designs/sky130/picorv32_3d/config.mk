export PLATFORM         = sky130hd
export DESIGN_NAME      = picorv32

# Point to your completed DEFs — skip synthesis+PnR
export DIE1_DEF = $(HOME)/Desktop/3DIC/pnr/picorv32_die1/picorv32_final.def
export DIE2_DEF = $(HOME)/Desktop/3DIC/pnr/sram_die/sram_die_final.def

export DIE_AREA         = 0 0 600 600
export CORE_AREA        = 10 10 590 590

# TSV connections from your assemble_3d.py
export TSV_COUNT        = 70
