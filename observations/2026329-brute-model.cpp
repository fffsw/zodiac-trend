// Independent full enumeration of C(49,6) sets, not a draw or prediction.
#include <iostream>
#include <cstdint>
using namespace std;
struct Sum { uint64_t dist[4]{}, single=0,pair=0,triple=0,both=0; };
int main(){
  // Z = 鼠牛虎兔龍蛇馬羊猴鷄狗豬; separately encoded from six numeric loops.
  uint16_t bit[50]{};for(int n=1;n<=49;n++)bit[n]=uint16_t(1u<<((7-n+120)%12));
  constexpr uint16_t mouse=1u<<0,tiger=1u<<2,dragon=1u<<4,snake=1u<<5,horse=1u<<6,sheep=1u<<7,monkey=1u<<8,chicken=1u<<9,dog=1u<<10;
  constexpr uint16_t prev=mouse|tiger|dragon|sheep|monkey|dog;Sum chosen,old,condition[7];uint64_t total=0;
  auto count=[](Sum& v,bool a,bool b,bool c){v.single+=a;v.pair+=b;v.triple+=c;v.both+=b&&c;v.dist[int(a)+int(b)+int(c)]++;};
  for(int a=1;a<=44;a++)for(int b=a+1;b<=45;b++)for(int c=b+1;c<=46;c++)for(int d=c+1;d<=47;d++)for(int e=d+1;e<=48;e++)for(int f=e+1;f<=49;f++){
    uint16_t m=bit[a]|bit[b]|bit[c]|bit[d]|bit[e]|bit[f];bool h=(m&horse)!=0;bool p=(m&(tiger|chicken))==(tiger|chicken);bool t=(m&(tiger|mouse|sheep))==(tiger|mouse|sheep);bool op=(m&(dog|chicken))==(dog|chicken);bool ot=(m&(dog|horse|snake))==(dog|horse|snake);count(chosen,h,p,t);count(old,h,op,ot);count(condition[__builtin_popcount((unsigned)(m&prev))],h,p,t);total++;
  }
  auto emit=[](const Sum&v){cout<<"{\"distribution\":["<<v.dist[0]<<","<<v.dist[1]<<","<<v.dist[2]<<","<<v.dist[3]<<"],\"single\":"<<v.single<<",\"pair\":"<<v.pair<<",\"triple\":"<<v.triple<<",\"pair_and_triple\":"<<v.both<<"}";};
  cout<<"{\"denominator\":"<<total<<",\"chosen\":";emit(chosen);cout<<",\"old\":";emit(old);cout<<",\"conditional\":[";for(int k=0;k<=6;k++){if(k)cout<<",";emit(condition[k]);}cout<<"]}\n";
}
