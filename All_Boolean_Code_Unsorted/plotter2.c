#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <math.h>
typedef FILE* fileptr;



int main(){
    int number_runs = 1400;
    int numnodes = 4;
    int constant_node_count = 1;
    // int run_files_per_link = 200;

    char idsfilename[200] = "GRHL2.ids";
    char filename[200] = "output/GRHL2_async_unweigh_ss_run";
    char jsdfilename[100] = "GRHL2_async_unweigh_jsd_";

    for(int i = 0; i < number_runs/200; i++){
        char tempfilename[200];
        char tempjsdappend[200];
        printf("%s\n", "meow");
        strcpy(tempfilename, jsdfilename);
        sprintf(tempjsdappend, "%d.txt", i + 1);
        strcat(tempfilename, tempjsdappend);
        fileptr tempfileptr;
        tempfileptr = fopen(tempfilename, "w");
        printf("%s\n", tempjsdappend);
        printf("%s\n", tempfilename);
        fclose(tempfileptr);
    }

    for(int run = 0; run < number_runs; run++){
        char curfile[200], tempappend[200];
        strcpy(curfile, filename);
        sprintf(tempappend, "%d.txt", run + 1);
        strcat(curfile, tempappend);
        // printf("%s\n", curfile);

        /* Reading node names from IDS file */
        fileptr idsfile;
        idsfile = fopen(idsfilename, "r");
        char nodes[numnodes][200], temp1[200], temp2[200];
        int tempnum;
        fscanf(idsfile, "%s %s", temp1, temp2);
        for(int i = 0; i < numnodes; i++){
            fscanf(idsfile, "%s %s", temp1, temp2);
            sscanf(temp2, "%d", &tempnum);
            strcpy(nodes[tempnum], temp1);
        }
        fclose(idsfile);

        /* Reading data from _ss_.txt file */
        fileptr ssfile;
        char tempread[200];
        int tempval[numnodes];
        ssfile = fopen(curfile, "r");
        for(int i = 0; i < numnodes + 1; i++){
            fscanf(ssfile, "%s", tempread);
            // printf("%s ", tempread);
        }
        //need arrays for probability count and the binary string, done below
        int tot_mem = 10, cur_mem = 0; // total mem to malloc arrays, and current mem location
        double *prob_matrix;
        char **bin_labels;

        prob_matrix = (double*) malloc(tot_mem * sizeof(double));
        bin_labels = (char**) malloc(tot_mem * sizeof(char*));

        for(int i = 0; i < tot_mem; i++){
            bin_labels[i] = (char*) malloc(numnodes * sizeof(char));
            prob_matrix[i] = 0;
        }
         // printf("meow\n");

        while(fscanf(ssfile, "%s", tempread) != EOF){

            // printf("meow\n");
            for(int i = 0; i < numnodes; i++){
                fscanf(ssfile, "%s", tempread);
                sscanf(tempread, "%d", &tempval[i]);
                // printf("%d\n", tempval[i]);
            }

            // printf("meow\n");
            char tempstr[50], temp_char; // temp thing for bin string
            int node_flag; // temp variable for converting -1/1 to 1/0
            strcpy(tempstr, "");
            for(int i = constant_node_count; i < numnodes; i++){
                temp_char = tempval[i] > 0? '1':'0';
                strncat(tempstr, &temp_char, 1);
            }
            // printf("%s\n", tempstr);
            int flag = 0;
            for(int i = 0; i < cur_mem; i++){
                if(strcmp(bin_labels[i], tempstr) == 0){
                    prob_matrix[i]++;
                    flag = 1;
                    break;
                }
            }
            if(flag == 0){
                if(cur_mem < tot_mem){
                    strcpy(bin_labels[cur_mem], tempstr);
                    prob_matrix[cur_mem]++;
                    cur_mem++;
                }
                else{
                    tot_mem += 10;
                    prob_matrix = (double*) realloc(prob_matrix, tot_mem * sizeof(double));
                    bin_labels = (char**) realloc(bin_labels, tot_mem * sizeof(char*));
                    // printf("meow\n");
                    for(int i = tot_mem - 10; i < tot_mem; i++){
                        bin_labels[i] = (char*) malloc(numnodes * sizeof(char));
                        prob_matrix[i] = 0;
                    }

                    strcpy(bin_labels[cur_mem], tempstr);
                    prob_matrix[cur_mem]++;
                    cur_mem++;
                }
            }
        }

        for(int i = 0; i < cur_mem; i++){
            // printf("%f\n", prob_matrix[i]);
            prob_matrix[i]/=(double)(10000);
            // printf("%f\n", prob_matrix[i]);
        }
        // printf("%s\n", "meow");
        /* Bit inefficient, but comparatively more reusable, incase you wanna get probability that is */

        int index_array[cur_mem];
        for(int i = 0; i < cur_mem; i++){
            index_array[i] = strtol(bin_labels[i], NULL, 2) - 1;
            // printf("%d %lf %s\n", index_array[i], prob_matrix[i], bin_labels[i]);
        }
        // exit(0);


        char jsdappend[200], jsdfilename_modified[200];
        int temprun = (run/200);
        temprun++;
        strcpy(jsdfilename_modified, jsdfilename);
        sprintf(jsdappend, "%d.txt", temprun);
        strcat(jsdfilename_modified, jsdappend);
        // printf("%d %s\n", temprun, jsdfilename_modified);
        fileptr jsdfile;
        jsdfile = fopen(jsdfilename_modified, "a");

        // A much more efficient way to do the next part would be to sort index_array and then have another counter
        // that keeps track of array number, if that makes sense. This way, you will probably have an O(n+mlogm) code.
        // This will be O(n*m), but that's kinda fine ig, it's fast enough anyway.
        // long totruns = (int)pow(2.0, (double)numnodes);
        int totruns = 1;
        for(int i = constant_node_count; i < numnodes; i++){
            totruns *= 2;
        }
        // for(int i = 0; i < cur_mem; i++){
        //     printf("%f\n", prob_matrix[i]);
        // }
        for(int i = 0; i < totruns - 1; i++){
            int flag = -1;
            for(int j = 0; j < cur_mem; j++){
                if(index_array[j] == i){
                    flag = (int)j;

                    // printf("flaggg %d\n", flag);
                    // printf("%d\n", flag);
                    break;
                }
            }
            if(flag == -1){
                fprintf(jsdfile, "%lf ", 0.0);
            }
            else{
                // printf("%d\n", flag);
                // printf("meowmeow %lf\n", prob_matrix[flag]);
                fprintf(jsdfile, "%lf ", prob_matrix[flag]);
            }
        }
        // for(int i = 0; i < cur_mem; i++){
        //     printf("%f\n", prob_matrix[i]);
        // }
        int flag = -1;
        for(int j = 0; j < cur_mem; j++){
            if(index_array[j] == (totruns - 1)){
                flag = j;
                break;
            }
        }
        if(flag == -1){
            fprintf(jsdfile, "%lf", 0.0);
        }
        else{
            // printf("%d\n", flag);
            fprintf(jsdfile, "%lf", prob_matrix[flag]);
        }
        fprintf(jsdfile, "\n");


        // exit(0);
        free(prob_matrix);
        free(bin_labels);
        fclose(ssfile);
        fclose(jsdfile);
        // printf("%s\n", "check");
        // exit(0);

    }
    // for(int i = 0; i < cur_mem; i++){
    //     printf("%d: %lf %s\n", i, prob_matrix[i], bin_labels[i]);
    // }

    // free(prob_matrix);
    // free(bin_labels);

    return 0;
}
