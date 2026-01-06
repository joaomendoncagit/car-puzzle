; benchmark generated from python API
(set-info :status unknown)
(declare-fun r_0_0 () Int)
(declare-fun c_0_0 () Int)
(declare-fun r_1_0 () Int)
(declare-fun c_1_0 () Int)
(declare-fun r_0_1 () Int)
(declare-fun c_0_1 () Int)
(declare-fun r_0_2 () Int)
(declare-fun c_0_2 () Int)
(declare-fun r_0_3 () Int)
(declare-fun c_0_3 () Int)
(declare-fun r_1_1 () Int)
(declare-fun c_1_1 () Int)
(declare-fun r_1_2 () Int)
(declare-fun c_1_2 () Int)
(declare-fun r_1_3 () Int)
(declare-fun c_1_3 () Int)
(declare-fun move_0_0 () Bool)
(declare-fun move_0_1 () Bool)
(declare-fun move_0_2 () Bool)
(declare-fun move_1_0 () Bool)
(declare-fun move_1_1 () Bool)
(declare-fun move_1_2 () Bool)
(assert
 (= r_0_0 0))
(assert
 (= c_0_0 2))
(assert
 (= r_1_0 2))
(assert
 (= c_1_0 0))
(assert
 (let (($x32 (>= r_0_0 0)))
 (and $x32 (< r_0_0 6))))
(assert
 (let (($x39 (>= c_0_0 0)))
 (and $x39 (< c_0_0 6))))
(assert
 (< (- (+ r_0_0 3) 1) 6))
(assert
 (let (($x117 (>= r_0_1 0)))
 (and $x117 (< r_0_1 6))))
(assert
 (let (($x125 (>= c_0_1 0)))
 (and $x125 (< c_0_1 6))))
(assert
 (< (- (+ r_0_1 3) 1) 6))
(assert
 (let (($x258 (>= r_0_2 0)))
 (and $x258 (< r_0_2 6))))
(assert
 (let (($x271 (>= c_0_2 0)))
 (and $x271 (< c_0_2 6))))
(assert
 (< (- (+ r_0_2 3) 1) 6))
(assert
 (let (($x423 (>= r_0_3 0)))
 (and $x423 (< r_0_3 6))))
(assert
 (let (($x415 (>= c_0_3 0)))
 (and $x415 (< c_0_3 6))))
(assert
 (< (- (+ r_0_3 3) 1) 6))
(assert
 (let (($x60 (>= r_1_0 0)))
 (and $x60 (< r_1_0 6))))
(assert
 (let (($x68 (>= c_1_0 0)))
 (and $x68 (< c_1_0 6))))
(assert
 (< (- (+ c_1_0 1) 1) 6))
(assert
 (let (($x142 (>= r_1_1 0)))
 (and $x142 (< r_1_1 6))))
(assert
 (let (($x149 (>= c_1_1 0)))
 (and $x149 (< c_1_1 6))))
(assert
 (< (- (+ c_1_1 1) 1) 6))
(assert
 (let (($x292 (>= r_1_2 0)))
 (and $x292 (< r_1_2 6))))
(assert
 (let (($x301 (>= c_1_2 0)))
 (and $x301 (< c_1_2 6))))
(assert
 (< (- (+ c_1_2 1) 1) 6))
(assert
 (let (($x401 (>= r_1_3 0)))
 (and $x401 (< r_1_3 6))))
(assert
 (let (($x394 (>= c_1_3 0)))
 (and $x394 (< c_1_3 6))))
(assert
 (< (- (+ c_1_3 1) 1) 6))
(assert
 (let (($x163 (= r_0_1 r_0_0)))
 (let (($x162 (= c_0_1 c_0_0)))
 (let (($x164 (and $x162 $x163)))
 (or $x164 (and $x162 (= r_0_1 (+ r_0_0 1))) (and $x162 (= r_0_1 (- r_0_0 1))))))))
(assert
 (= move_0_0 (or (and (distinct r_0_1 r_0_0) true) (and (distinct c_0_1 c_0_0) true))))
(assert
 (let (($x255 (= r_0_2 r_0_1)))
 (let (($x257 (= c_0_2 c_0_1)))
 (let (($x256 (and $x257 $x255)))
 (or $x256 (and $x257 (= r_0_2 (+ r_0_1 1))) (and $x257 (= r_0_2 (- r_0_1 1))))))))
(assert
 (= move_0_1 (or (and (distinct r_0_2 r_0_1) true) (and (distinct c_0_2 c_0_1) true))))
(assert
 (let (($x469 (= r_0_3 r_0_2)))
 (let (($x468 (= c_0_3 c_0_2)))
 (let (($x470 (and $x468 $x469)))
 (or $x470 (and $x468 (= r_0_3 (+ r_0_2 1))) (and $x468 (= r_0_3 (- r_0_2 1))))))))
(assert
 (= move_0_2 (or (and (distinct r_0_3 r_0_2) true) (and (distinct c_0_3 c_0_2) true))))
(assert
 (let (($x189 (= c_1_1 c_1_0)))
 (let (($x188 (= r_1_1 r_1_0)))
 (let (($x190 (and $x188 $x189)))
 (or $x190 (and $x188 (= c_1_1 (+ c_1_0 1))) (and $x188 (= c_1_1 (- c_1_0 1))))))))
(assert
 (= move_1_0 (or (and (distinct r_1_1 r_1_0) true) (and (distinct c_1_1 c_1_0) true))))
(assert
 (let (($x324 (= c_1_2 c_1_1)))
 (let (($x323 (= r_1_2 r_1_1)))
 (let (($x325 (and $x323 $x324)))
 (or $x325 (and $x323 (= c_1_2 (+ c_1_1 1))) (and $x323 (= c_1_2 (- c_1_1 1))))))))
(assert
 (= move_1_1 (or (and (distinct r_1_2 r_1_1) true) (and (distinct c_1_2 c_1_1) true))))
(assert
 (let (($x488 (= c_1_3 c_1_2)))
 (let (($x419 (= r_1_3 r_1_2)))
 (let (($x494 (and $x419 $x488)))
 (or $x494 (and $x419 (= c_1_3 (+ c_1_2 1))) (and $x419 (= c_1_3 (- c_1_2 1))))))))
(assert
 (= move_1_2 (or (and (distinct r_1_3 r_1_2) true) (and (distinct c_1_3 c_1_2) true))))
(assert
 (or (not move_0_0) (not move_1_0)))
(assert
 (or move_0_0 move_1_0))
(assert
 (or (not move_0_1) (not move_1_1)))
(assert
 (or move_0_1 move_1_1))
(assert
 (or (not move_0_2) (not move_1_2)))
(assert
 (or move_0_2 move_1_2))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 0) r_1_0) true) $x84))))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 1) r_1_0) true) $x84))))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 2) r_1_0) true) $x84))))
(assert
 (let ((?x219 (+ c_1_1 0)))
 (let (($x221 (and (distinct c_0_1 ?x219) true)))
 (or (and (distinct (+ r_0_1 0) r_1_1) true) $x221))))
(assert
 (let ((?x219 (+ c_1_1 0)))
 (let (($x221 (and (distinct c_0_1 ?x219) true)))
 (or (and (distinct (+ r_0_1 1) r_1_1) true) $x221))))
(assert
 (let ((?x219 (+ c_1_1 0)))
 (let (($x221 (and (distinct c_0_1 ?x219) true)))
 (or (and (distinct (+ r_0_1 2) r_1_1) true) $x221))))
(assert
 (let ((?x354 (+ c_1_2 0)))
 (let (($x356 (and (distinct c_0_2 ?x354) true)))
 (or (and (distinct (+ r_0_2 0) r_1_2) true) $x356))))
(assert
 (let ((?x354 (+ c_1_2 0)))
 (let (($x356 (and (distinct c_0_2 ?x354) true)))
 (or (and (distinct (+ r_0_2 1) r_1_2) true) $x356))))
(assert
 (let ((?x354 (+ c_1_2 0)))
 (let (($x356 (and (distinct c_0_2 ?x354) true)))
 (or (and (distinct (+ r_0_2 2) r_1_2) true) $x356))))
(assert
 (let ((?x509 (+ c_1_3 0)))
 (let (($x511 (and (distinct c_0_3 ?x509) true)))
 (or (and (distinct (+ r_0_3 0) r_1_3) true) $x511))))
(assert
 (let ((?x509 (+ c_1_3 0)))
 (let (($x511 (and (distinct c_0_3 ?x509) true)))
 (or (and (distinct (+ r_0_3 1) r_1_3) true) $x511))))
(assert
 (let ((?x509 (+ c_1_3 0)))
 (let (($x511 (and (distinct c_0_3 ?x509) true)))
 (or (and (distinct (+ r_0_3 2) r_1_3) true) $x511))))
(assert
 (= r_1_3 2))
(assert
 (= c_1_3 5))
(check-sat)
