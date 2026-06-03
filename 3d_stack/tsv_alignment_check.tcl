# TSV Alignment Verification — Die-1 ↔ Die-2
# Run inside OpenROAD after loading Die-1 DEF

set DIE_HEIGHT_DBU  600000
set BOND_Y_MIN_DIE1 520000
set BOND_Y_MAX_DIE1 600000
set BOND_Y_MIN_DIE2 0
set BOND_Y_MAX_DIE2 80000
set TOLERANCE_DBU   500

# TSV connection map: Die-1 pin -> Die-2 pin
array set TSV_MAP {
    clk          clk0
    mem_valid    csb0
    mem_ready    web0
    mem_wstrb\[0\]  wmask0\[0\]
    mem_wstrb\[1\]  wmask0\[1\]
    mem_wstrb\[2\]  wmask0\[2\]
    mem_wstrb\[3\]  wmask0\[3\]
    mem_addr\[0\]   addr0\[0\]
    mem_addr\[1\]   addr0\[1\]
    mem_addr\[2\]   addr0\[2\]
    mem_addr\[3\]   addr0\[3\]
    mem_addr\[4\]   addr0\[4\]
    mem_addr\[5\]   addr0\[5\]
    mem_addr\[6\]   addr0\[6\]
    mem_addr\[7\]   addr0\[7\]
    mem_wdata\[0\]  din0\[0\]
    mem_wdata\[1\]  din0\[1\]
    mem_wdata\[2\]  din0\[2\]
    mem_wdata\[3\]  din0\[3\]
    mem_wdata\[4\]  din0\[4\]
    mem_wdata\[5\]  din0\[5\]
    mem_wdata\[6\]  din0\[6\]
    mem_wdata\[7\]  din0\[7\]
    mem_wdata\[8\]  din0\[8\]
    mem_wdata\[9\]  din0\[9\]
    mem_wdata\[10\] din0\[10\]
    mem_wdata\[11\] din0\[11\]
    mem_wdata\[12\] din0\[12\]
    mem_wdata\[13\] din0\[13\]
    mem_wdata\[14\] din0\[14\]
    mem_wdata\[15\] din0\[15\]
    mem_wdata\[16\] din0\[16\]
    mem_wdata\[17\] din0\[17\]
    mem_wdata\[18\] din0\[18\]
    mem_wdata\[19\] din0\[19\]
    mem_wdata\[20\] din0\[20\]
    mem_wdata\[21\] din0\[21\]
    mem_wdata\[22\] din0\[22\]
    mem_wdata\[23\] din0\[23\]
    mem_wdata\[24\] din0\[24\]
    mem_wdata\[25\] din0\[25\]
    mem_wdata\[26\] din0\[26\]
    mem_wdata\[27\] din0\[27\]
    mem_wdata\[28\] din0\[28\]
    mem_wdata\[29\] din0\[29\]
    mem_wdata\[30\] din0\[30\]
    mem_wdata\[31\] din0\[31\]
    mem_rdata\[0\]  dout0\[0\]
    mem_rdata\[1\]  dout0\[1\]
    mem_rdata\[2\]  dout0\[2\]
    mem_rdata\[3\]  dout0\[3\]
    mem_rdata\[4\]  dout0\[4\]
    mem_rdata\[5\]  dout0\[5\]
    mem_rdata\[6\]  dout0\[6\]
    mem_rdata\[7\]  dout0\[7\]
    mem_rdata\[8\]  dout0\[8\]
    mem_rdata\[9\]  dout0\[9\]
    mem_rdata\[10\] dout0\[10\]
    mem_rdata\[11\] dout0\[11\]
    mem_rdata\[12\] dout0\[12\]
    mem_rdata\[13\] dout0\[13\]
    mem_rdata\[14\] dout0\[14\]
    mem_rdata\[15\] dout0\[15\]
    mem_rdata\[16\] dout0\[16\]
    mem_rdata\[17\] dout0\[17\]
    mem_rdata\[18\] dout0\[18\]
    mem_rdata\[19\] dout0\[19\]
    mem_rdata\[20\] dout0\[20\]
    mem_rdata\[21\] dout0\[21\]
    mem_rdata\[22\] dout0\[22\]
    mem_rdata\[23\] dout0\[23\]
    mem_rdata\[24\] dout0\[24\]
    mem_rdata\[25\] dout0\[25\]
    mem_rdata\[26\] dout0\[26\]
    mem_rdata\[27\] dout0\[27\]
    mem_rdata\[28\] dout0\[28\]
    mem_rdata\[29\] dout0\[29\]
    mem_rdata\[30\] dout0\[30\]
    mem_rdata\[31\] dout0\[31\]
}

# ── Get pin locations from loaded design ──────────────────────
proc get_pin_location {pin_name} {
    set block [ord::get_db_block]
    set bterm [$block findBTerm $pin_name]
    if {$bterm == "NULL"} {
        return ""
    }
    set pins [$bterm getBPins]
    set pin [lindex $pins 0]
    set boxes [$pin getBoxes]
    set box [lindex $boxes 0]
    set x [expr {([$box xMin] + [$box xMax]) / 2}]
    set y [expr {([$box yMin] + [$box yMax]) / 2}]
    return [list $x $y]
}

# ── Load Die-1 pins ───────────────────────────────────────────
puts "\n============================================================"
puts "  TSV Alignment Verification — Die-1 picorv32"
puts "============================================================"

# Load Die-1
read_liberty /home/kartheesan/pdks/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
read_lef /home/kartheesan/pdks/sky130A/libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef
read_lef /home/kartheesan/pdks/sky130A/libs.ref/sky130_fd_sc_hd/lef/sky130_fd_sc_hd.lef
read_def ~/Desktop/3DIC/3d_stack/picorv32_with_tsvpads.def

# Collect Die-1 bonding zone pins
array set die1_pins {}
set block [ord::get_db_block]
foreach bterm [$block getBTerms] {
    set name [$bterm getName]
    set loc [get_pin_location $name]
    if {$loc == ""} continue
    set y [lindex $loc 1]
    if {$y >= $BOND_Y_MIN_DIE1 && $y <= $BOND_Y_MAX_DIE1} {
        set die1_pins($name) $loc
    }
}
puts "  Die-1 bonding-zone pads found: [array size die1_pins]"

# ── Load Die-2 pins ───────────────────────────────────────────
puts "\n  Loading Die-2 SRAM..."
read_lef /home/kartheesan/Desktop/3DIC/sram_die/sram_8k/sky130_sram_1kbyte_1rw1r_32x256_8.lef
read_def ~/Desktop/3DIC/3d_stack/sram_with_tsvpads.def

array set die2_pins {}
set block [ord::get_db_block]
foreach bterm [$block getBTerms] {
    set name [$bterm getName]
    set loc [get_pin_location $name]
    if {$loc == ""} continue
    set y [lindex $loc 1]
    if {$y >= $BOND_Y_MIN_DIE2 && $y <= $BOND_Y_MAX_DIE2} {
        set die2_pins($name) $loc
    }
}
puts "  Die-2 bonding-zone pads found: [array size die2_pins]"

# ── Verify alignment ──────────────────────────────────────────
set passed  0
set failed  0
set missing 0

set report_lines {}

puts "\n------------------------------------------------------------"
puts [format "  %-22s %-18s %8s %8s %10s" \
    "Die-1 Pin" "Die-2 Pin" "ΔX" "ΔY" "Status"]
puts "------------------------------------------------------------"

foreach {d1_pin d2_pin} [array get TSV_MAP] {
    if {![info exists die1_pins($d1_pin)]} {
        puts [format "  %-22s %-18s %8s %8s %10s" \
            $d1_pin $d2_pin "-" "-" "D1_MISSING"]
        incr missing
        lappend report_lines "$d1_pin,$d2_pin,,,,,D1_MISSING"
        continue
    }
    if {![info exists die2_pins($d2_pin)]} {
        puts [format "  %-22s %-18s %8s %8s %10s" \
            $d1_pin $d2_pin "-" "-" "D2_MISSING"]
        incr missing
        lappend report_lines "$d1_pin,$d2_pin,,,,,D2_MISSING"
        continue
    }

    set x1 [lindex $die1_pins($d1_pin) 0]
    set y1 [lindex $die1_pins($d1_pin) 1]
    set x2 [lindex $die2_pins($d2_pin) 0]
    set y2 [lindex $die2_pins($d2_pin) 1]

    # Mirror rule: y2_expected = DIE_HEIGHT - y1
    set y2_exp [expr {$DIE_HEIGHT_DBU - $y1}]
    set dx [expr {abs($x2 - $x1)}]
    set dy [expr {abs($y2 - $y2_exp)}]

    if {$dx <= $TOLERANCE_DBU && $dy <= $TOLERANCE_DBU} {
        set status "PASS ✅"
        incr passed
    } else {
        set status "FAIL ❌"
        incr failed
    }

    puts [format "  %-22s %-18s %8d %8d %10s" \
        $d1_pin $d2_pin $dx $dy $status]
    lappend report_lines "$d1_pin,$d2_pin,$x1,$y1,$x2,$y2,$dx,$dy,[expr {$dx<=$TOLERANCE_DBU && $dy<=$TOLERANCE_DBU ? \"PASS\" : \"FAIL\"}]"
}

# ── Summary ───────────────────────────────────────────────────
puts "\n============================================================"
puts "  RESULTS:"
puts "    PASS    : $passed / 70"
puts "    FAIL    : $failed / 70"
puts "    MISSING : $missing / 70"
puts "============================================================"

# Write CSV report
set report_path "~/Desktop/3DIC/tsv_alignment_report.csv"
set f [open [file normalize $report_path] w]
puts $f "die1_pin,die2_pin,x1_dbu,y1_dbu,x2_dbu,y2_dbu,delta_x,delta_y,status"
foreach line $report_lines {
    puts $f $line
}
close $f
puts "\n  Report saved: $report_path"

if {$passed == 70 && $failed == 0 && $missing == 0} {
    puts "\n  🎉 All 70 TSV connections verified — perfect alignment!"
} elseif {$failed == 0} {
    puts "\n  ✅ $passed connections aligned ($missing without pair)"
} else {
    puts "\n  ⚠  $failed misaligned — check tsv_alignment_report.csv"
}
puts "============================================================\n"
