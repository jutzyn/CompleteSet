/*
 * CS_Main.cpp
 *
 *  Created on: 2012-6-5
 *      Author: yuningz
 */

#include "stdio.h"
#include "string.h"
#include "time.h"

static int loop;
unsigned char set[27] = {'a','b','c','d','e',
                         'f','g','h','i','j',
                         'k','l','m','n','o',
                         'p','q','r','s','t',
                         'u','v','w','x','y',
                         'z',0};

void CompleteSet(unsigned char *Set, int start, int end, int precount = 0)
{
    int j = 0;
    if(start == end)
    {
        if(precount == 0)
        {
            printf("{ %c }\n", *(Set+start));
        }
        else
        {
            printf("{");
            for(int i = precount; i >= 0; i--)
            {
                printf(" %c ", *(Set+start-i));
            }
            printf("}\n");
        }
        loop++;
    }
    else
    {
        CompleteSet(Set,start,start,precount);
        CompleteSet(Set,start+1,end, precount+1);
        if(precount > 0)
        {
            unsigned char temp;
            temp = *(Set+start);
            for(j = 0; j < precount; j++)
            {
                *(Set+start - j) = *(Set+start - j - 1);
            }
            *(Set+start - j) = temp;
            CompleteSet(Set, start+1,end, precount);
            temp = *(Set+start - j);
            for(j = precount; j > 0; j--)
            {
                *(Set+start - j) = *(Set+start - j + 1);
            }
            *(Set+start) = temp;
        }
        else
            CompleteSet(Set, start+1,end, precount);
    }
}
int main(void)
{
    clock_t before, after;
    loop = 0;
    before = clock();
    CompleteSet(set,4,9);
    after = clock();
    printf(" Take %d ms \n", (int)(after - before));
    printf(" loop count is %d \n", loop);
    return 0;
}






