import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable, Modal } from 'react-native';
import { HoleCard, HoleCardState } from './HoleCard';
import { HoleProgress } from './HoleProgress';
import { ScoreLabel } from '../shared/ScoreLabel';
import { Button } from '../shared/Button';
import { ActiveRound, ScoredHoleEntry, saveActiveRound, clearActiveRound, enqueueOfflineHole, getOfflineQueue, removeFromQueue } from '../../lib/storage';
import { useScoreHole, useFinishRound } from '../../lib/queries';

type Props = {
  round: ActiveRound;
  onRoundUpdate: (updated: ActiveRound) => void;
  onFinish: (roundId: string) => void;
  onAbandon: () => void;
};

export function LiveScorecard({ round, onRoundUpdate, onFinish, onAbandon }: Props) {
  const scoreHole = useScoreHole();
  const finishRound = useFinishRound();

  const currentIndex = round.scored_holes.length;
  const currentHoleStub = round.tee_box_holes[currentIndex];
  const isLastHole = currentIndex === round.holes_total - 1;
  const [showAbandon, setShowAbandon] = useState(false);

  const [cardState, setCardState] = useState<HoleCardState>({
    score: currentHoleStub?.par ?? 4,
    gir: false,
    fairway: currentHoleStub?.par !== 3 ? 'o' : null,
    putts: 2,
  });

  if (!currentHoleStub) return null;

  const runningToPar = round.scored_holes.reduce((sum, h) => sum + h.toPar, 0);

  async function submitHole() {
    const toPar = cardState.score - currentHoleStub.par;
    const payload = {
      round_id: round.round_id,
      tee_box_hole_id: currentHoleStub.id,
      score: cardState.score,
      gir: cardState.gir,
      putts: cardState.putts,
      ...(cardState.fairway !== null ? { fairway: cardState.fairway } : {}),
    };

    const entry: ScoredHoleEntry = { holeNumber: currentHoleStub.number, toPar };
    const updated: ActiveRound = {
      ...round,
      scored_holes: [...round.scored_holes, entry],
    };

    await saveActiveRound(updated);
    onRoundUpdate(updated);

    await enqueueOfflineHole(payload);  // save first
    try {
      await scoreHole.mutateAsync(payload);
      // On API success, remove it from the offline queue
      // The queue processor will handle syncing, but we can remove the just-submitted item
      const queue = await getOfflineQueue();
      const idx = queue.findIndex((q) => q.tee_box_hole_id === payload.tee_box_hole_id && q.round_id === payload.round_id);
      if (idx !== -1) await removeFromQueue(idx);
    } catch {
      // already in queue — will sync on reconnect
    }

    if (isLastHole) {
      try {
        await finishRound.mutateAsync({ roundId: round.round_id });
      } catch {
        // v1 known gap: PATCH not queued offline
      }
      await clearActiveRound();
      onFinish(round.round_id);
    } else {
      const nextHoleStub = round.tee_box_holes[currentIndex + 1];
      setCardState({
        score: nextHoleStub.par,
        gir: false,
        fairway: nextHoleStub.par !== 3 ? 'o' : null,
        putts: 2,
      });
    }
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      {/* Header */}
      <View className="px-4 pt-12 pb-2 flex-row items-center justify-between">
        <View>
          <Text className="text-lg font-bold text-[#111] dark:text-white">Round</Text>
          <Text className="text-[#888] text-sm">Thru {round.scored_holes.length}</Text>
        </View>
        <View className="flex-row items-center gap-3">
          <ScoreLabel toPar={runningToPar} size="lg" />
          <Pressable onPress={() => setShowAbandon(true)} hitSlop={8}>
            <Text className="text-[#888] text-xl">···</Text>
          </Pressable>
        </View>
      </View>

      <HoleProgress
        total={round.holes_total}
        currentHole={currentHoleStub.number}
        scoredHoles={round.scored_holes}
      />

      <View className="px-4 py-4">
        <HoleCard
          holeNumber={currentHoleStub.number}
          par={currentHoleStub.par}
          yards={currentHoleStub.yards}
          state={cardState}
          onChange={setCardState}
        />
      </View>

      <View className="px-4 pb-8">
        <Button
          label={isLastHole ? 'Finish Round' : 'Next Hole \u2192'}
          onPress={submitHole}
          loading={scoreHole.isPending || finishRound.isPending}
        />
      </View>

      <Modal visible={showAbandon} transparent animationType="fade">
        <View className="flex-1 bg-black/50 items-center justify-center px-6">
          <View className="bg-white dark:bg-[#1c1c1e] rounded-2xl p-6 w-full">
            <Text className="text-lg font-bold text-[#111] dark:text-white mb-2">Abandon round?</Text>
            <Text className="text-[#888] mb-6">The round will remain incomplete in the backend.</Text>
            <Button label="Yes, abandon" onPress={async () => { await clearActiveRound(); setShowAbandon(false); onAbandon(); }} />
            <Pressable className="mt-3 items-center" onPress={() => setShowAbandon(false)}>
              <Text className="text-[#888]">Cancel</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}
