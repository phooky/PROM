#version 130

out vec4 out_color;
uniform uint ww;
uniform uint wh;
uniform uint stride;
uniform uint romh;

uniform usampler2D romtex;
uniform uint sel0;
uniform uint sel1;

void main() {
    uint texw = 16384u;
     uint x = uint(gl_FragCoord[0] - 0.5);
     uint y = (wh - 1u) - uint(gl_FragCoord[1] - 0.5);
     uint col = x / stride;
     uint bitidx = ((y  + (col*wh)) * stride) + (x % stride);
     
     uint tex_off = bitidx / 8u;
     uint tex_bit_off = bitidx % 8u;

     if (tex_off >= {}u) {
     	out_color = vec4(0.0,0.0,0.4,1.0);
     	return;
	}	
    uint tex_off_x = tex_off % texw;
    uint tex_off_y = tex_off / texw;
    uint rv = (texelFetch(romtex, ivec2(int(tex_off_x),int(tex_off_y)),0).r >> (7u-tex_bit_off)) & 1u;
    vec4 c = vec4(float(rv),float(rv),float(rv), 1.0);
    if (bitidx >= sel0 && bitidx < sel1) {
        c.b = 0.0; c.g = 0.0;
    }
     out_color = c; 
}
