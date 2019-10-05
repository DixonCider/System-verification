CC := g++-9 --std=c++17
exe := ./verifier
files := main.cpp
headers := periodic.h weaklyhard.h

$(exe): $(files) $(headers)
	$(CC) $(files) -O2 -o $(exe)

run: $(exe)
	$(exe) periodic input/case_01.in
	$(exe) periodic input/case_02.in
	$(exe) periodic input/case_03.in
	$(exe) periodic input/case_04.in
	$(exe) periodic input/case_05.in
	$(exe) periodic input/case_06.in
	$(exe) periodic input/case_07.in
	$(exe) periodic input/case_08.in
	$(exe) periodic input/case_09.in
	$(exe) periodic input/case_10.in
	$(exe) periodic input/case_11.in

clean:
	rm -f $(exe)