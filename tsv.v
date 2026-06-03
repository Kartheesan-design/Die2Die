module tsv #(parameter DELAY=0) (
    input in,
    output out
);

assign #(DELAY) out = in;

endmodule
