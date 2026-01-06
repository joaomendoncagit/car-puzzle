; benchmark generated from python API
(set-info :status unknown)
(declare-fun r_0_0 () Int)
(declare-fun c_0_0 () Int)
(declare-fun r_1_0 () Int)
(declare-fun c_1_0 () Int)
(declare-fun r_0_1 () Int)
(declare-fun c_0_1 () Int)
(declare-fun r_1_1 () Int)
(declare-fun c_1_1 () Int)
(declare-fun move_0_0 () Bool)
(declare-fun move_1_0 () Bool)
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
 (let (($x163 (= r_0_1 r_0_0)))
 (let (($x162 (= c_0_1 c_0_0)))
 (let (($x164 (and $x162 $x163)))
 (or $x164 (and $x162 (= r_0_1 (+ r_0_0 1))) (and $x162 (= r_0_1 (- r_0_0 1))))))))
(assert
 (= move_0_0 (or (and (distinct r_0_1 r_0_0) true) (and (distinct c_0_1 c_0_0) true))))
(assert
 (let (($x189 (= c_1_1 c_1_0)))
 (let (($x188 (= r_1_1 r_1_0)))
 (let (($x190 (and $x188 $x189)))
 (or $x190 (and $x188 (= c_1_1 (+ c_1_0 1))) (and $x188 (= c_1_1 (- c_1_0 1))))))))
(assert
 (= move_1_0 (or (and (distinct r_1_1 r_1_0) true) (and (distinct c_1_1 c_1_0) true))))
(assert
 (or (not move_0_0) (not move_1_0)))
(assert
 (or move_0_0 move_1_0))
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
 (= r_1_1 2))
(assert
 (= c_1_1 5))
(check-sat)
