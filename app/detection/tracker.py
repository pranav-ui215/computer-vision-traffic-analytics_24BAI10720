from dataclasses import dataclass,field
import math

@dataclass
class Track:
    track_id:int
    centroid:tuple
    bbox:tuple
    label:str="object"
    missing:int=0
    history:list=field(default_factory=list)

class CentroidTracker:
    def __init__(self,max_distance=80,max_missing=12):
        self.max_distance=max_distance; self.max_missing=max_missing
        self.next_id=1; self.tracks={}
    @staticmethod
    def center(b):
        x1,y1,x2,y2=b; return ((x1+x2)//2,(y1+y2)//2)
    def update(self,detections):
        candidates=[]
        for d in detections:
            x1,y1,x2,y2=d.bbox
            candidates.append((d,(x1,y1,x2,y2),self.center((x1,y1,x2,y2))))
        unmatched=set(self.tracks)
        for d,b,c in candidates:
            best=None; bestdist=float("inf")
            for tid in unmatched:
                dist=math.dist(c,self.tracks[tid].centroid)
                if dist<bestdist and dist<=self.max_distance: best,bestdist=tid,dist
            if best is None:
                tid=self.next_id; self.next_id+=1
                t=Track(tid,c,b,getattr(d,"label","object"),0,[c]); self.tracks[tid]=t
            else:
                tid=best; t=self.tracks[tid]; t.centroid=c;t.bbox=b;t.label=getattr(d,"label",t.label);t.missing=0;t.history.append(c)
                if len(t.history)>30:t.history.pop(0)
                unmatched.remove(tid)
        for tid in list(unmatched):
            self.tracks[tid].missing+=1
            if self.tracks[tid].missing>self.max_missing: del self.tracks[tid]
        return list(self.tracks.values())
