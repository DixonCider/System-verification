#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    vector<pair<int, int>> nextState;
    vector<int> unsafeState;
    for (int i = 0; i < n; i++) {
        int x, y, s;
        scanf("%d%d%d", &x, &y, &s);
        nextState.push_back({x, y});
        if (s) {
            unsafeState.push_back(i);
        }
    }
    int k;
    vector<pair<int, int>> eventList;
    scanf("%d", &k);
    for (int i = 0; i < k; i++) {
        int s, o;
        scanf("%d%d", &s, &o);
        eventList.push_back({s, o});
    }

    puts("MODULE main");
    puts("VAR");
    puts("\tisunsafe: boolean;");
    printf("\tstate: {");
    for (int i = 0; i < n; i++) {
        if (i) printf(", ");
        printf("S%d", i);
    }
    puts("};");   
    printf("\tperiodic: {");
    for (int i = 0; i < k; i++) {
        if (i) printf(", ");
        printf("P%d", i);
    }
    puts("};");
    puts("ASSIGN");
    puts("\tinit(isunsafe) := FALSE;");
    puts("\tinit(state) := S0;");
    puts("\tinit(periodic) := P0;");
    printf("\tnext(state) := case\n");
    for (int i = 0; i < n; i++) {
        printf("\t\t(state = S%d & event = FALSE): S%d;\n", i, nextState[i].first);
        printf("\t\t(state = S%d & event = TRUE): S%d;\n", i, nextState[i].second);
    }
    puts("\tesac;");
    printf("\tnext(periodic) := case\n");
    for (int i = 0; i < k; i++) {
        printf("\t\t(periodic = P%d): P%d;\n", i, eventList[i].first);
    }
    puts("\tesac;");
    printf("\tnext(isunsafe) := case\n");
    for (int unsafe: unsafeState) {
        printf("\t\t(state = S%d): TRUE;\n", unsafe);
    }
    printf("\t\tTRUE: isunsafe;\n");
    puts("\tesac;");
    puts("DEFINE");
    printf("\tevent := case\n");
    for (int i = 0; i < k; i++) {
        printf("\t\t(periodic = P%d): %s;\n", i, eventList[i].second ? "TRUE": "FALSE");
    }
    puts("\tesac;\n");
    puts("LTLSPEC G (isunsafe = FALSE)");
}