#include <bits/stdc++.h>

#include "periodic.h"
#include "weaklyhard.h"

using namespace std;


int main(int argc, char **argv) {

    if (strcmp(argv[1], "periodic") == 0) {
        if (argc != 3) {
            cerr << "[Error] Please run the program with command: ./main periodic input_file" << endl;
            return 0;
        }
        int n, k;
        ifstream fin(argv[2]);
        fin >> n;
        vector<pair<pair<int, int>, int>> transition;
        vector<pair<int, int>> event;
        for (int i = 0; i < n; i++) {
            int s0, s1, unsafe;
            fin >> s0 >> s1 >> unsafe;
            transition.push_back({{s0, s1}, unsafe});
        }
        fin >> k;
        for (int i = 0; i < k; i++) {
            int s0, o0;
            fin >> s0 >> o0;
            event.push_back({s0, o0});
        }

        Verification::Periodic solver(n, k);
        for (int i = 0; i < n; i++) {
            solver.addEdgeMachine(i, transition[i].first.first, transition[i].first.second, transition[i].second);
        }
        for (int i = 0; i < k; i++) {
            solver.addEdgeEvent(i, event[i].first, event[i].second);
        }
        solver.solve();
        solver.solveAll();
    } else if (strcmp(argv[1], "weaklyhardsingle") == 0) {
        if (argc != 4) {
            cerr << "[Error] Please run the program with command: ./main weaklyhardsingle input_file K" << endl;
            return 0;
        }
        int n;
        ifstream fin(argv[2]);
        fin >> n;
        vector<pair<pair<int, int>, int>> transition;
        vector<pair<int, int>> event;
        for (int i = 0; i < n; i++) {
            int s0, s1, unsafe;
            fin >> s0 >> s1 >> unsafe;
            transition.push_back({{s0, s1}, unsafe});
        }

        int K = atoi(argv[3]);


        vector<vector<int>> result(K + 1);
        for (int k = 1; k <= K; k++) {
            for (int m = 0; m <= k; m++) {
                printf("(%d, %d)\n", m, k);
                Verification::WeaklyHardSingle solver(n, m, k);
                for (int i = 0; i < n; i++) {
                    solver.addEdgeMachine(i, transition[i].first.first, transition[i].first.second, transition[i].second);
                }
                result[k].push_back(solver.solve());
            }
        }

        for (int i = 1; i <= K; i++) {
            printf("K = %d\t:", i);
            for (int x: result[i]) {
                printf(" %d", x);
            }
            puts("");
        }
    }  else if (strcmp(argv[1], "weaklyhardmono") == 0) {
        if (argc != 4) {
            cerr << "[Error] Please run the program with command: ./main weaklyhardsingle input_file K" << endl;
            return 0;
        }
        int n;
        ifstream fin(argv[2]);
        fin >> n;
        vector<pair<pair<int, int>, int>> transition;
        vector<pair<int, int>> event;
        for (int i = 0; i < n; i++) {
            int s0, s1, unsafe;
            fin >> s0 >> s1 >> unsafe;
            transition.push_back({{s0, s1}, unsafe});
        }

        int K = atoi(argv[3]);


        vector<vector<int>> result(K + 1);
        int prev = 0;
        for (int k = 1; k <= K; k++) {
            for (int x: result[k - 1]) {
                result[k].push_back(x);
            }
            if (result[k].size() && result[k].back()) result[k].pop_back();
            for (int m = prev; m <= k; m++) {
                printf("(%d, %d)\n", m, k);
                Verification::WeaklyHardSingle solver(n, m, k);
                for (int i = 0; i < n; i++) {
                    solver.addEdgeMachine(i, transition[i].first.first, transition[i].first.second, transition[i].second);
                }
                result[k].push_back(solver.solve());
                prev = m;
                if (result[k].back()) break;
            }
        }

        for (int i = 1; i <= K; i++) {
            printf("K = %d\t:", i);
            for (int x: result[i]) {
                printf(" %d", x);
            }
            puts("");
        }
    }   else if (strcmp(argv[1], "weaklyhardreuse") == 0) {
        if (argc != 4) {
            cerr << "[Error] Please run the program with command: ./main weaklyhardsingle input_file K" << endl;
            return 0;
        }
        int n;
        ifstream fin(argv[2]);
        fin >> n;
        vector<pair<pair<int, int>, int>> transition;
        vector<pair<int, int>> event;
        for (int i = 0; i < n; i++) {
            int s0, s1, unsafe;
            fin >> s0 >> s1 >> unsafe;
            transition.push_back({{s0, s1}, unsafe});
        }

        int K = atoi(argv[3]);


        vector<vector<int>> result(K + 1);
        int prev = 0;
        for (int k = 1; k <= K; k++) {
            printf("(%d)\n", k);
            Verification::WeaklyHardReuse solver(n, k);
            for (int i = 0; i < n; i++) {
                solver.addEdgeMachine(i, transition[i].first.first, transition[i].first.second, transition[i].second);
            }
            int ret = solver.solve();
            for (int i = 0; i < ret; i++) {
                result[k].push_back(0);
            }
            if (ret != k + 1) {
                result[k].push_back(1);
            }
        }

        for (int i = 1; i <= K; i++) {
            printf("K = %d\t:", i);
            for (int x: result[i]) {
                printf(" %d", x);
            }
            puts("");
        }
    } else {
        cerr << "[Error] Please run the program with command: ./main type input_file" << endl;
    }
}