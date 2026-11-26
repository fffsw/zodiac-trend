// Full direct 49-choose-6 enumeration. This hypothetical model is NOT a draw or a forecast.
#include <iostream>
#include <cstdint>
using namespace std;
struct C {uint64_t dist[4]{},single=0,pair=0,triple=0,both=0;};
int main(){
 uint16_t bit[50]{};for(int n=1;n<=49;n++)bit[n]=uint16_t(1u<<((7-n+120)%12));
 constexpr uint16_t ox=1u<<1,rabbit=1u<<3,dragon=1u<<4,snake=1u<<5,horse=1u<<6,monkey=1u<<8,chicken=1u<<9,dog=1u<<10,pig=1u<<11,prev=horse|monkey|pig|ox|chicken;
 C old,newv,oc[6],nc[6];uint64_t total=0;
 auto count=[](C&v,bool a,bool b,bool c){v.dist[int(a)+int(b)+int(c)]++;v.single+=a;v.pair+=b;v.triple+=c;v.both+=b&&c;};
 for(int a=1;a<=44;a++)for(int b=a+1;b<=45;b++)for(int c=b+1;c<=46;c++)for(int d=c+1;d<=47;d++)for(int e=d+1;e<=48;e++)for(int f=e+1;f<=49;f++){
  uint16_t m=bit[a]|bit[b]|bit[c]|bit[d]|bit[e]|bit[f];bool s=(m&horse);bool op=(m&(chicken|ox))==(chicken|ox);bool ot=(m&(chicken|dragon|snake))==(chicken|dragon|snake);bool np=(m&(dog|ox))==(dog|ox);bool nt=(m&(dog|rabbit|snake))==(dog|rabbit|snake);int k=__builtin_popcount((unsigned)(m&prev));count(old,s,op,ot);count(newv,s,np,nt);count(oc[k],s,op,ot);count(nc[k],s,np,nt);total++;
 }
 auto emit=[](const C&v){cout<<"{\"distribution\":["<<v.dist[0]<<","<<v.dist[1]<<","<<v.dist[2]<<","<<v.dist[3]<<"],\"single\":"<<v.single<<",\"pair\":"<<v.pair<<",\"triple\":"<<v.triple<<",\"pair_and_triple\":"<<v.both<<"}";};
 cout<<"{\"denominator\":"<<total<<",\"old\":";emit(old);cout<<",\"revised\":";emit(newv);cout<<",\"old_conditional\":[";for(int k=0;k<=5;k++){if(k)cout<<",";emit(oc[k]);}cout<<"],\"revised_conditional\":[";for(int k=0;k<=5;k++){if(k)cout<<",";emit(nc[k]);}cout<<"]}\n";
}
