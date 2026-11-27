// Directly enumerate all 49-choose-6 sets under a hypothetical equal-probability model.
// The 331 previous-normal identities are conditioned on; this does NOT query a draw or predict 332.
#include <iostream>
#include <cstdint>
using namespace std;
struct Stats {uint64_t dist[4]{},single=0,pair=0,triple=0,both=0;};
struct Case {const char* name; uint16_t s,p,t;};
int main(){
 uint16_t bit[50]{};for(int n=1;n<=49;n++)bit[n]=uint16_t(1u<<((7-n+120)%12));
 constexpr uint16_t ox=1u<<1,tiger=1u<<2,rabbit=1u<<3,dragon=1u<<4,snake=1u<<5,horse=1u<<6,sheep=1u<<7,monkey=1u<<8,chicken=1u<<9,dog=1u<<10,pig=1u<<11,prev=ox|rabbit|dragon|snake|monkey;
 Case cases[]={{"HH00",horse,uint16_t(dog|ox),uint16_t(dog|rabbit|snake)}, {"HH01",horse,uint16_t(tiger|ox),uint16_t(tiger|chicken|sheep)}, {"HH08",sheep,uint16_t(tiger|ox),uint16_t(tiger|horse|chicken)}, {"T14",horse,uint16_t(tiger|ox),uint16_t(chicken|sheep|pig)}, {"T15",horse,uint16_t(tiger|ox),uint16_t(horse|chicken|sheep)}};
 constexpr int N=sizeof(cases)/sizeof(cases[0]);Stats all[N],conditional[N][6];uint64_t total=0;
 auto count=[](Stats&v,bool a,bool b,bool c){v.dist[int(a)+int(b)+int(c)]++;v.single+=a;v.pair+=b;v.triple+=c;v.both+=b&&c;};
 for(int a=1;a<=44;a++)for(int b=a+1;b<=45;b++)for(int c=b+1;c<=46;c++)for(int d=c+1;d<=47;d++)for(int e=d+1;e<=48;e++)for(int f=e+1;f<=49;f++){
  uint16_t m=bit[a]|bit[b]|bit[c]|bit[d]|bit[e]|bit[f];int k=__builtin_popcount((unsigned)(m&prev));
  for(int i=0;i<N;i++){bool s=(m&cases[i].s)==cases[i].s,p=(m&cases[i].p)==cases[i].p,t=(m&cases[i].t)==cases[i].t;count(all[i],s,p,t);count(conditional[i][k],s,p,t);}total++;
 }
 auto emit=[](const Stats&v){cout<<"{\"distribution\":["<<v.dist[0]<<","<<v.dist[1]<<","<<v.dist[2]<<","<<v.dist[3]<<"],\"single\":"<<v.single<<",\"pair\":"<<v.pair<<",\"triple\":"<<v.triple<<",\"pair_and_triple\":"<<v.both<<"}";};
 cout<<"{\"denominator\":"<<total<<",\"cases\":{";for(int i=0;i<N;i++){if(i)cout<<",";cout<<"\""<<cases[i].name<<"\":{"<<"\"overall\":";emit(all[i]);cout<<",\"conditional\":[";for(int k=0;k<=5;k++){if(k)cout<<",";emit(conditional[i][k]);}cout<<"]}";}cout<<"}}\n";
}
