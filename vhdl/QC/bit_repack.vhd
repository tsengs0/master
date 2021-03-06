library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use IEEE.math_real.all;


entity bit_repack is
	generic (
		LAST_WORD_PADDING : natural := 0
	);
	port (
		clk : in std_logic;
		res : in std_logic;
		in_bits : in std_logic_vector;
		out_bits : out std_logic_vector;
		in_rdy : out std_logic;
		in_wr : in std_logic;
		in_last : in std_logic;
		out_rdy : in std_logic;
		out_wr : out std_logic;
		out_last : out std_logic
	);
end entity;

architecture base of bit_repack is
    attribute mark_debug : string;
    attribute keep : string;
	signal bit_store : std_logic_vector(out_bits'length + in_bits'length - 1 downto 0);
	signal out_wr_int, out_last_int : std_logic;
	signal store_cnt : unsigned(12 downto 0) := (others => '0');
	signal in_rdy_int : std_logic := '0';
	signal zero_pad : std_logic_vector(out_bits'range) := (others => '0');
	signal flusing : std_logic := '0';
	
	attribute mark_debug of store_cnt : signal is "true";
	attribute mark_debug of flusing : signal is "true";
begin
	out_wr <= out_wr_int;
	in_rdy <= in_rdy_int;
	out_last <= out_last_int;

	in_rdy_int <= '1' when in_bits'length <= bit_store'length + out_bits'length - store_cnt  and res = '0' and flusing = '0' else '0';
	out_last_int <= '1' when flusing = '1' and store_cnt = LAST_WORD_PADDING else '0';
	out_wr_int <= '1' when (store_cnt >= out_bits'length or (flusing = '1' and store_cnt = LAST_WORD_PADDING)) and res = '0' else '0';
	process (clk)
		variable store_cnt_tmp : unsigned(store_cnt'range);
		variable bit_store_tmp : std_logic_vector(bit_store'range);
	begin
		if rising_edge(clk) then
			if in_last = '1' and in_wr = '1' then
				flusing <= '1';
			end if;
			if out_last_int = '1' then
				--out_last_int <= '0';
			end if;
			bit_store_tmp := bit_store;
			store_cnt_tmp := store_cnt;
			if (store_cnt >= out_bits'length or flusing = '1') and res = '0' and out_rdy = '1' then
				--out_wr_int <= '1';
				bit_store_tmp := std_logic_vector(shift_left(unsigned(bit_store_tmp), out_bits'length));
				out_bits <= bit_store(bit_store'length-1 downto bit_store'length - out_bits'length);
				store_cnt_tmp := store_cnt_tmp - out_bits'length;
			else
				--out_wr_int <= '0';
			end if;
			if in_wr = '1' and in_rdy_int = '1' then
				bit_store_tmp := bit_store_tmp or std_logic_vector(shift_right(unsigned(in_bits & zero_pad), to_integer(store_cnt_tmp)));
				store_cnt_tmp := store_cnt_tmp + in_bits'length;
			end if;
			if flusing = '1' and store_cnt = LAST_WORD_PADDING and out_rdy = '1' then
				store_cnt_tmp := (others => '0');
				flusing <= '0';
				--out_last_int <= '1';
            else
                --out_last_int <= '0';
			end if;
			if res = '1' then
				flusing <= '0';
				--out_last_int <= '0';
				bit_store <= (others => '0');
				store_cnt <= (others => '0');
			else
				bit_store <= bit_store_tmp;
				store_cnt <= store_cnt_tmp;
			end if;
			


		end if;
	end process;

end architecture;
