#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include "pcg_basic.h"
#include <omp.h>
#include <math.h>

typedef FILE* fileptr;
//GRHL2_async_unweigh_nss_run585
double max(double a, double b){
	
	if(a>b){
		return a;
	}
	else{
		return b;
	}
	
	
}
double min(double a, double b){
	
	if(a<b){
		return a;
	}
	else{
		return b;
	}
	
	
}

int main(){
	double begin1=omp_get_wtime();

	
		//printf("aAAEABRO \n");
	int updation_rule=2;
    int nsim = 1000;
    int maxtime = 2000;

    int numnodes;   //automatically set later
	int numthreads;
	int async;
	int sync;
	int weighted;
	int unweighted;
	int selective;
	int numruns;
	int constantnode;
    char filename[5000];
	char input[5000];
	char output[5000];
	char randomise[5000];
	int ac=10;

    double *link_matrix;
    char **nodes;
	

    /* READING FROM init.txt */
    fileptr init;
	// fileptr jsdfile;
    char temp1[300], temp2[300], temp3[300];
    int tempint;

    init = fopen("init.txt", "r");
    if(init == NULL){
        fprintf(stderr, "ERROR: Can't open init.txt!\n");
        exit(0);
    }
	fscanf(init, "%s %s\n", temp1, input);
    fscanf(init, "%s %s\n", temp1, output);
    fscanf(init, "%s %s\n", temp1, filename);
    fscanf(init, "%s %d\n", temp1, &numthreads);
	fscanf(init, "%s %d\n", temp1, &numruns);
	fscanf(init, "%s %d\n", temp1, &nsim);
    fscanf(init, "%s %d\n", temp1, &maxtime);
    fscanf(init, "%s %d\n", temp1, &async);
    fscanf(init, "%s %d\n", temp1, &sync);
    fscanf(init, "%s %d\n", temp1, &weighted);
    fscanf(init, "%s %d\n", temp1, &unweighted);
    fscanf(init, "%s %d\n", temp1, &selective);
	fscanf(init, "%s %s\n", temp1,  randomise);
    fscanf(init, "%s %d\n", temp1, &constantnode);
	
	
			
	//printf("sfss \n");
    /* setting topo and ids file name variables */
    char topofilename[5000];
    strcpy(topofilename, filename);
    strcat(topofilename, ".topo");

    char idsfilename[5000];
    strcpy(idsfilename, filename);
    strcat(idsfilename, ".ids");


    /* PARSING IDS FILE */
    fileptr idsfile = fopen(idsfilename, "r");
	
	
    if(idsfile == NULL){
        fprintf(stderr, "ERROR: ids file cannot be opened, or is missing.\n");
        exit(0);
    }

	
	
	char temp4[300], temp5[300];
	int count=0;
	
	fscanf(idsfile, "%s %s\n", temp4, temp5);
	
    while(fscanf(idsfile, "%s %s\n", temp4, temp5) != EOF){
        sscanf(temp5, "%d", &tempint);
        count++;
    }
	
	//printf("%d \n",count);
	numnodes=count;
	
	fclose(idsfile);
	idsfile = fopen(idsfilename, "r");
	nodes = (char**)malloc((numnodes) * sizeof(char*));
    for(int i = 0; i < numnodes; i++){
        nodes[i] = (char*)malloc(50 * sizeof(char));
    }
	
	
	
    fscanf(idsfile, "%s %s\n", temp1, temp2);
    while(fscanf(idsfile, "%s %s\n", temp1, temp2) != EOF){
        sscanf(temp2, "%d", &tempint);
        strcpy(nodes[tempint], temp1);
    }
	
	
	
	

    /* PARSING TOPO FILE */
    fileptr topofile;
    topofile = fopen(topofilename, "r");
    if(topofile == NULL){
        fprintf(stderr, "ERROR: topo file cannot be opened, or is missing.\n");
        exit(0);
    }

    int n = numnodes;
    link_matrix = (double *)malloc(n * n * sizeof(double));
    if(link_matrix == NULL){
        fprintf(stderr, "ERROR: link matrix couldn't be initialised (malloc error).\n");
        exit(0);
    }

    for(int i = 0; i < n * n; i++){
        link_matrix[i] = 0;
    }
    int index1 = 0, index2 = 0;

    fscanf(topofile, "%s %s %s\n", temp1, temp2, temp3);

    while(fscanf(topofile, "%s %s %s\n", temp1, temp2, temp3) != EOF){
        sscanf(temp3, "%d", &tempint);
        for(int i = 0; i < n; i++){
            if(strcmp(nodes[i], temp1) == 0){
                index1 = i;
            }
            if(strcmp(nodes[i], temp2) == 0){
                index2 = i;
            }
        }
        link_matrix[index1 * n + index2] = tempint == 1? 1: -1;
    }
	
    pcg32_random_t rng;
	double time1=(omp_get_wtime()-begin1)*100000;
    pcg32_srandom_r(&rng, time(NULL) ^ (intptr_t)&printf, (intptr_t)&time1);

		for (int pp=0;pp<numruns;pp++){	
	
			//printf("hi\n");
	int cnt=0;
	int level=pp/(2*ac) +1 ;
	int saveq=0;
	int savesign=0;
	/*
	for(int q=0;q<n*n;q++){
		if(link_matrix[q]!=0){
			cnt++;
			
			
		}
		if(cnt==level){
			saveq=q;
			int f=-1;
			if(link_matrix[q]>0){
				f=1;
			}
			savesign=f;
	
			link_matrix[q]=f*(pp-(2*ac)*(level-1))/((float)(ac));
			
			break;
		}
	}
	
	*/
	
	
	double deg[numnodes];
	
	for(int q=0;q<numnodes;q++){
		
		deg[q]=0;
	}
	for(int q=0;q<numnodes;q++){
		for(int m=0;m<numnodes;m++){
			
		deg[q]+=fabs(link_matrix[m*numnodes+q]);
		//printf("%f ",link_matrix[m*numnodes+q]);
		//printf("\n");
	}
	}
	//for(int q=0;q<numnodes;q++){
	//			printf("%f ",deg[q]);
	//		}
	for(int q=0;q<numnodes;q++){
		deg[q]=0.25*pow(deg[q],0.5);
	}
//	for(int q=0;q<numnodes;q++){
	//			printf("%f ",deg[q]);
		//	}
	/*
	printf("\n");
	for(int gg=0;gg<n*n;gg++){
//	//	fflush(stdout);
	printf("%f ",link_matrix[gg]);
	//	fflush(stdout);
	}
	printf("\n");
*/
	//printf("hi1\n");
    // initialise(&nsim, &maxtime, &numnodes, &filename, link_matrix, nodes);
    // printf("meow\n");
	
	
    //printf("Nodes with ID:\n");
    //for(int i = 0; i < numnodes; i++){
     //   printf("%d %s\n", i, nodes[i]);
    //}
	
	

    // for(int i = 0; i < numnodes; i++){
    //     for(int j = 0; j < numnodes; j++){
    //         printf("%f ", link_matrix[i * numnodes + j]);
    //     }
    //     printf("\n");
    // }

    char initname[100], ssname[100], fssname[100], nssname[100];
    strcpy(initname, "output/");
    strcpy(ssname, "output/");
	strcpy(fssname, "output/");
    strcpy(nssname, "output/");
	//printf("hi2\n");
char snum[100];
sprintf(snum, "%d", pp+1);
//char printfile[100];
//itoa(num, snum, 10);
	//printf("hi4\n");
//strcat(printfile, filename);
	//strcat(printfile, "_async_unweigh_run");
		//strcat(printfile, snum);
		//printf("hi5\n");
	//printf("%s",printfile);
    strcat(initname, filename);
	strcat(initname, "_async_unweigh_init_run");
	strcat(initname, snum);
	strcat(initname, ".txt");
	//////printf("hi6\n");

	strcat(ssname, filename);
	strcat(ssname, "_async_unweigh_ss_run");
	strcat(ssname, snum);
	strcat(ssname, ".txt");
	////printf("hi7\n");
	
	strcat(fssname, filename);
	strcat(fssname, "_async_unweigh_fss_run");
	strcat(fssname, snum);
	strcat(fssname, ".txt");
	
	////printf("hig7\n");
	strcat(nssname, filename);
	strcat(nssname, "_async_unweigh_nss_run");
	strcat(nssname, snum);
	strcat(nssname, ".txt");
	////printf("hi8\n");
    fileptr initstate, ss, nss,fss;
    initstate = fopen(initname, "w");
	//printf("%s ",ssname);
    ss = fopen(ssname, "w");
	fss = fopen(fssname, "w");
    nss = fopen(nssname, "w");
	 //fprintf(ss, "ID ");
	 
//	printf("hi9\n");
    /* Initial file inputs */
	////printf("hi9\n");
    fprintf(initstate, "ID ");
	//	printf("hi99999\n");
    fprintf(ss, "ID ");
	fprintf(fss, "ID ");
	//	printf("hi9\n");
    fprintf(nss, "ID ");
//printf("hi10\n");
    for(int i = 0; i < numnodes-1; i++){
        fprintf(initstate, "%s ", nodes[i]);
        fprintf(ss, "%s ", nodes[i]);
        fprintf(nss, "%s ", nodes[i]);
		fprintf(fss, "%s ", nodes[i]);
    }
	  for(int i = numnodes-1; i < numnodes; i++){
        fprintf(initstate, "%s", nodes[i]);
        fprintf(ss, "%s", nodes[i]);
        fprintf(nss, "%s", nodes[i]);
		fprintf(fss, "%s", nodes[i]);
    }
	//printf("hi103\n");
		//printf("hi10\n");
    fprintf(initstate, " Stable");
    fprintf(initstate, "\n");
    fprintf(ss, "\n");
    fprintf(nss, "\n");
	fprintf(fss, "\n");
    // return 0;
//	printf("hi11\n");
    int simnum = 0;
    int idnum = 1;


/*
	int length1=(int)(pow(2,numnodes-constantnode)+0.000001);
	char str[length1][numnodes];
	for(int q=0;q<length1;q++){
		
		int q1=q;
		int m=1;
		
		while(m<=numnodes){
		if(q1%2==1){
				str[q][numnodes-m]='1';
		}
		else{
			str[q][numnodes-m]='0';
		}
	
		q1=q1/2;
		m++;
		}
		
	}
	*/
	/*
	for(int u=0;u<1;u++){
		
		printf("%s \n",str[u]);
//		fflush(stdout);
		printf("\n");
	}
	*/
/*
double probarr[length1];
for(int u=0;u<length1;u++){
	
	probarr[u]=0;
}
*/
	
	//printf("hi3\n");
    while(simnum < nsim){
        // simnum++;
        fprintf(initstate, "%d ", idnum);

		int stable_checker = 1;
		double activation[numnodes];
		double curstate[numnodes];

        //randomise curstate
        for(int i = 0; i < numnodes; i++){
			//pcg32_boundedrand_r(pcg32_random_t* rng, uint32_t bound)
          //curstate[i] = pcg32_boundedrand_r(&rng, 2) ? 1 : -1;
		   curstate[i]=ldexp(pcg32_random_r(&rng), -32) *2 -1;
			//printf("%f \n",curstate[i]);
            fprintf(initstate, "%d ", ((int)(curstate[i]>0.5))*2 -1);
        }

	int rr=0;
        //matmul and stable state checker
      for(int iter = 0; iter < maxtime; iter++){
            stable_checker = 1;
            for(int i = 0; i < numnodes; i++){
                activation[i] = 0;
                for(int j = 0; j < numnodes; j++){
                    activation[i] += link_matrix[j * numnodes + i] * curstate[j];
                }
				//activation[i]-=0.1*pow(2,curstate[i]);
                // printf("%d ", activation[i]);
                if(activation[i] * curstate[i] < 0 && fabs(activation[i])>=deg[i] ){ //
                    stable_checker = 0;
					
                }
				// stable_checker = 0;
				
            }
			
		
		/*	if(iter>maxtime/1.1){
				printf("%d ",iter);
			for(int q=0;q<numnodes;q++){
		
				printf("%f ",curstate[q]);
			}
			printf("\n");
		
			for(int q=0;q<numnodes;q++){
		
				printf("%f ",activation[q]);
			}
			printf("\n");
				printf("____________________\n");
			}
			*/
		//	for(int q=0;q<numnodes;q++){
		//		printf("%d ",activation[q]);
		//	}
		//	printf("\n ________________________________\n");
            // printf("\n");
			  if(stable_checker){
				  rr++;
				  
			  }
			  	if(rr<10){
				
				//stable_checker =0;
			}
            if(stable_checker){ /*
					printf("\n");
	for(int gg=0;gg<n*n;gg++){
//	//	fflush(stdout);
	printf("%f ",link_matrix[gg]);
	//	fflush(stdout);
	}
	
	printf("\n");

				printf("\n");
				for(int q=0;q<numnodes;q++){
				printf("%f ",curstate[q]);
			}
			printf("\n");
			for(int q=0;q<numnodes;q++){
				printf("%f ",activation[q]);
			}
			printf("\n ________________________________\n");
            // printf("\n");
			*/
			
				//int tempi=length1/2;
				//int aa=0;
				// for(int i = constantnode; i < numnodes; i++){
               //     aa+=tempi*((int)(curstate[i]>0));
				//	tempi/=2;
              //  }
			//	probarr[aa]+=1;
                fprintf(ss, "%d ", idnum);
				fprintf(fss, "%d ", idnum);
                for(int i = 0; i < numnodes-1; i++){
                    fprintf(ss, "%d ", ((int)(curstate[i]>0)*2) -1 );
					fprintf(fss, "%f ", curstate[i]);
                }
				  fprintf(ss, "%d",(int)(curstate[numnodes-1]>0)*2 -1);
				  fprintf(fss, "%f", curstate[numnodes-1]);
                fprintf(ss, "\n");
				fprintf(fss, "\n");
                fprintf(initstate, "1\n");
                idnum++;
                simnum++;
                break;
            }
            else{
				     int rand_node;
					 int qq=0;
		        switch (updation_rule) {
                    case 0: //sync updation
                        for(int i = 0; i < numnodes; i++){
                            if (activation[i] > 0){
                                curstate[i] = 1;
                            }
                            else if(activation[i] < 0){
                                curstate[i] = -1;
                            }
                        }
                        break;
                    case 1: //async updation
						
						while(qq==0){
						rand_node=  pcg32_boundedrand_r(&rng, numnodes);
						//printf("%d \n",rand_node);
                        if (activation[rand_node] > 0 && curstate[rand_node]<0){
                            curstate[rand_node] = 1;
							qq=1;
                        }
                        else if(activation[rand_node] < 0  && curstate[rand_node]>0){
                            curstate[rand_node] = -1;
							qq=1;
                        }
						}
						break;
						case 2: //sync updation continuous
							for(int i = 0; i < numnodes; i++){
							
							//if( fabs(activation[i])>=deg[i]){
								
									
							
							if(fabs(activation[i])>0){
								
								curstate[i]+= 0.1 * activation[i]/(fabs(activation[i]) +1);
								
							}
							
									if(curstate[i]>1){
								curstate[i]=1;
							}
							
							if(curstate[i]<-1){
								curstate[i]=-1;
							}
								
								
					
                      //  }
							}
							break;
					case 3: //async updation continuous
							while(qq==0){
							
							rand_node=  1+pcg32_boundedrand_r(&rng, numnodes-1);
								if(iter>maxtime/1.1){
									printf("%d %d\n",iter,rand_node);
									
								}
								
							if(activation[rand_node]>0 && fabs(curstate[rand_node])<1){
								qq=1;
								
							}
							if(qq==1){
							if(fabs(activation[rand_node])>=-1){
								if(activation[rand_node]>0){
									curstate[rand_node]+=0.1;
								}
								if(activation[rand_node]<0){
									curstate[rand_node]+=-0.1;
								}
								
								
								
							}
							if(curstate[rand_node]>1){
								curstate[rand_node]=1;
							}
							else if (curstate[rand_node]<-1){
								
								curstate[rand_node]=-1;
							}
							break;
							}
							
							}
                        break;	
                       
                
            }
        }
		}

        if(stable_checker == 0){
			//printf("sdsds \n");
            fprintf(nss, "%d ", idnum);
            for(int i = 0; i < numnodes-1; i++){
                fprintf(nss, "%d ", (int)(curstate[i]>0)*2 -1);
            }
			fprintf(nss, "%d", (int)(curstate[numnodes-1]>0)*2 -1);
            fprintf(nss, "\n");
            fprintf(initstate, "0\n");
            idnum++;
        }
// fflush(stdout);
        if(simnum % (nsim/100) == 0){
           printf("\r %s %d %d%% %f s ",filename,pp+1,((simnum * 100)/nsim),omp_get_wtime()-begin1);
		   fflush(stdout);
        }

    }
//printf("miracle \n");



//for(int q=0;q<length1;q++){
	
	//probarr[q]/=simnum;
//}

//for(int q=0;q<length1;q++){
	
	//printf("%f \n",probarr[q]);
	//printf("%d \n",length1);
//}
//printf("%d 0 \n",pp);
//char jsd[200];
//char snum1[200];
//sprintf(snum1, "%d", (int)((pp)/(2*ac)+1));
 //strcat(jsd, filename);
//	strcat(jsd, "_async_unweigh_jsd_");
	
//	strcat(jsd, snum1);
//	strcat(jsd, ".txt");
//printf("%s \n",jsd);
//printf("%d \n",(int)((pp)/200.0+1));
//printf("%d 1 \n ",pp);
   
	//if(pp%(2*ac)==0){
		
		//  jsdfile = fopen(jsd, "w");
	//}
	//else{
//		jsdfile = fopen(jsd, "a");
	//}
    //jsdfile = fopen(jsd, "a");
	//for(int q=0;q<length1-1;q++){
	//fprintf(jsdfile,"%f ",probarr[q]);
	//}
	//printf("%d 2 \n ",pp);
//fprintf(jsdfile,"%f\n",probarr[length1-1]);

 //memset(jsd, 0, 200);
  //memset(snum1, 0, 200);
  
//  printf("%d 3  \n",pp);
link_matrix[saveq]=savesign;

    fclose(initstate);
//	fclose(jsdfile);
    fclose(ss);
    fclose(nss);
	fclose(fss);
	//fclose(jsdfile);
//	fclose(jsdfile);
//printf("%d 4 \n ",pp);
//printf("dsds\n");
//free(jsdfile);
//printf("mirac44le \n");
}
//free(jsdfile);
	fclose(init);
fclose(idsfile);
fclose(topofile);
	

    free(link_matrix);
    free(nodes);
    return 0;
		
}



/* TEMPORARY FUNCTION STORAGE */
// void initialise(int *nsim, int *maxtime, int *numnodes, char *filename, double *link_matrix, char **nodes){
//
//     /* READING FROM init.txt */
//     fileptr init;
//     char temp1[30], temp2[30], temp3[30];
//     int tempint;
//     init = fopen("init.txt", "r");
//     if(init == NULL){
//         fprintf(stderr, "ERROR: Can't open init.txt!\n");
//         exit(0);
//     }
//     fscanf(init, "%s %d\n", temp1, nsim);
//     fscanf(init, "%s %d\n", temp1, maxtime);
//     fscanf(init, "%s %s\n", temp1, filename);
//     fscanf(init, "%s %d\n", temp1, numnodes);
//
//     char topofilename[50];
//     strcpy(topofilename, filename);
//     strcat(topofilename, ".topo");
//
//     char idsfilename[50];
//     strcpy(idsfilename, filename);
//     strcat(idsfilename, ".ids");
//
//     /* PARSING IDS FILE */
//     fileptr idsfile = fopen(idsfilename, "r");
//     if(idsfile == NULL){
//         fprintf(stderr, "ERROR: ids file cannot be opened, or is missing.\n");
//         exit(0);
//     }
//
//     nodes = (char**)malloc((*numnodes) * sizeof(char*));
//     for(int i = 0; i < *numnodes; i++){
//         nodes[i] = (char*)malloc(50 * sizeof(char));
//     }
//     fscanf(idsfile, "%s %s\n", temp1, temp2);
//     while(fscanf(idsfile, "%s %s\n", temp1, temp2) != EOF){
//         sscanf(temp2, "%d", &tempint);
//         strcpy(nodes[tempint], temp1);
//     }
//     // for(int i = 0; i < *numnodes; i++){
//     //     printf("%s\n", nodes[i]);
//     // }
//
//     /* PARSING TOPO FILE */
//     fileptr topofile;
//     topofile = fopen(topofilename, "r");
//     if(topofile == NULL){
//         fprintf(stderr, "ERROR: topo file cannot be opened, or is missing.\n");
//         exit(0);
//     }
//
//     int n = *numnodes;
//     link_matrix = (double *)malloc(n * n * sizeof(double));
//     if(link_matrix == NULL){
//         fprintf(stderr, "ERROR: link matrix couldn't be initialised (malloc error).\n");
//         exit(0);
//     }
//     // link_matrix[3] = 0;
//     for(int i = 0; i < n * n; i++){
//         link_matrix[i] = 0;
//         // printf("%f\n", link_matrix[i]);
//     }
//     int index1 = 0, index2 = 0;
//
//     fscanf(topofile, "%s %s %s\n", temp1, temp2, temp3);
//     // printf("meow\n");
//     while(fscanf(topofile, "%s %s %s\n", temp1, temp2, temp3) != EOF){
//         // printf("meow2\n");
//         // printf("%s %s %s\n", temp1, temp2, temp3);
//         sscanf(temp3, "%d", &tempint);
//         for(int i = 0; i < n; i++){
//             if(strcmp(nodes[i], temp1) == 0){
//                 index1 = i;
//             }
//             if(strcmp(nodes[i], temp2) == 0){
//                 index2 = i;
//             }
//         }
//         // printf("%d %d\n", index1, index2);
//         link_matrix[index1 * n + index2] = tempint == 1? 1: -1;
//     }
//     // for(int i = 0; i < n; i++){
//     //     for(int j = 0; j < n; j++){
//     //         printf("%f ", link_matrix[i * n + j]);
//     //     }
//     //     printf("\n");
//     // }
//
//     // exit(0);
//
// }
